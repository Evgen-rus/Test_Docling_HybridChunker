import re
from datetime import datetime
from typing import List, Dict

class SimpleChunk:
    """Простой класс для хранения чанка"""
    def __init__(self, text: str, heading: str, stage_number: int):
        self.text = text
        self.heading = heading
        self.stage_number = stage_number
        self.size = len(text)

class SimpleChunker:
    """
    Простой чанкер, который разбивает документ по заголовкам этапов
    """
    
    def __init__(self):
        # Паттерн для поиска заголовков этапов
        self.stage_pattern = r'^## Этап (\d+)'
        
    def chunk_by_stages(self, file_path: str) -> List[SimpleChunk]:
        """
        Разбивает документ на чанки по этапам
        
        Args:
            file_path: путь к markdown файлу
            
        Returns:
            список SimpleChunk объектов
        """
        print(f"📄 Читаю файл: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✂️ Разбиваю по этапам...")
        
        # Разбиваем на строки
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        current_heading = ""
        current_stage = 0
        
        for line in lines:
            # Проверяем, является ли строка заголовком этапа
            stage_match = re.match(self.stage_pattern, line)
            
            if stage_match:
                # Сохраняем предыдущий чанк (если есть)
                if current_chunk and current_heading:
                    chunk_text = '\n'.join(current_chunk).strip()
                    if chunk_text:  # Только если есть содержимое
                        chunks.append(SimpleChunk(
                            text=chunk_text,
                            heading=current_heading,
                            stage_number=current_stage
                        ))
                
                # Начинаем новый чанк
                current_stage = int(stage_match.group(1))
                current_heading = line.strip()
                current_chunk = [line]
            else:
                # Добавляем строку к текущему чанку
                current_chunk.append(line)
        
        # Не забываем последний чанк
        if current_chunk and current_heading:
            chunk_text = '\n'.join(current_chunk).strip()
            if chunk_text:
                chunks.append(SimpleChunk(
                    text=chunk_text,
                    heading=current_heading,
                    stage_number=current_stage
                ))
        
        print(f"✅ Создано {len(chunks)} чанков по этапам")
        return chunks

def save_chunks_to_markdown(chunks: List[SimpleChunk], filename: str = "simple_chunks.md"):
    """
    Сохраняет чанки в красивый Markdown файл
    
    Args:
        chunks: список SimpleChunk объектов
        filename: имя выходного файла
    """
    with open(filename, "w", encoding="utf-8") as f:
        # Заголовок документа
        f.write("# Простое разбиение документа по этапам\n\n")
        f.write(f"**Дата создания:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Всего этапов:** {len(chunks)}\n\n")
        
        # Статистика
        total_chars = sum(chunk.size for chunk in chunks)
        avg_size = total_chars // len(chunks) if chunks else 0
        
        f.write("## 📊 Статистика\n\n")
        f.write(f"- **Общее количество символов:** {total_chars:,}\n")
        f.write(f"- **Средний размер этапа:** {avg_size:,} символов\n")
        f.write(f"- **Самый большой этап:** {max(chunk.size for chunk in chunks):,} символов\n")
        f.write(f"- **Самый маленький этап:** {min(chunk.size for chunk in chunks):,} символов\n\n")
        
        f.write("---\n\n")
        
        # Содержание
        f.write("## 📋 Содержание\n\n")
        for chunk in chunks:
            f.write(f"- [Этап {chunk.stage_number}](#этап-{chunk.stage_number})\n")
        f.write("\n---\n\n")
        
        # Детальные этапы
        for i, chunk in enumerate(chunks, 1):
            f.write(f"## Этап {chunk.stage_number}\n\n")
            
            # Метаданные
            f.write("### 📊 Информация об этапе\n\n")
            f.write(f"- **Номер этапа:** {chunk.stage_number}\n")
            f.write(f"- **Размер:** {chunk.size:,} символов\n")
            f.write(f"- **Заголовок:** {chunk.heading}\n\n")
            
            # Содержимое этапа
            f.write("### 📝 Полное содержимое\n\n")
            f.write("```markdown\n")
            f.write(chunk.text)
            f.write("\n```\n\n")
            
            # Разделитель между этапами
            if i < len(chunks):
                f.write("---\n\n")
    
    print(f"📁 Все этапы сохранены в файл: {filename}")

def main():
    """Основная функция"""
    print("🚀 Начинаю простое разбиение документа по этапам...")
    
    # Путь к файлу
    input_file = "documents/ЛОГИКА_ПРОДАЖИ_ТЕСТОВОГО_ПЕРИОДА_ЛИДГЕНБЮРО.md"
    
    # Создаем чанкер
    chunker = SimpleChunker()
    
    try:
        # Разбиваем документ
        chunks = chunker.chunk_by_stages(input_file)
        
        if not chunks:
            print("❌ Не найдено ни одного этапа в документе!")
            return
        
        # Показываем статистику
        print("\n" + "="*60)
        print("📊 СТАТИСТИКА РАЗБИЕНИЯ:")
        print("="*60)
        
        total_chars = sum(chunk.size for chunk in chunks)
        
        print(f"📋 Всего этапов: {len(chunks)}")
        print(f"📏 Общий размер: {total_chars:,} символов")
        print(f"📐 Средний размер этапа: {total_chars // len(chunks):,} символов")
        
        print(f"\n🔍 Размеры этапов:")
        for chunk in chunks:
            print(f"   Этап {chunk.stage_number}: {chunk.size:,} символов")
        
        # Сохраняем результат
        print("\n" + "="*60)
        print("💾 СОХРАНЕНИЕ РЕЗУЛЬТАТА:")
        print("="*60)
        
        save_chunks_to_markdown(chunks, "simple_chunks_by_stages.md")
        
        print("\n✅ Готово! Документ разбит по этапам.")
        print("📄 Результат сохранен в: simple_chunks_by_stages.md")
        
    except FileNotFoundError:
        print(f"❌ Файл не найден: {input_file}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 