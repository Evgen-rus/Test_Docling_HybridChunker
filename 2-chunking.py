from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from openai import OpenAI
import json
from datetime import datetime

load_dotenv()

# Initialize OpenAI client
client = OpenAI()

print("🚀 Начинаю процесс разбиения документа на фрагменты...")

# --------------------------------------------------------------
# Извлечение данных из локального документа
# --------------------------------------------------------------

converter = DocumentConverter()
print("📄 Обрабатываю документ...")
result = converter.convert("documents/ЛОГИКА_ПРОДАЖИ_ТЕСТОВОГО_ПЕРИОДА_ЛИДГЕНБЮРО.md")

# --------------------------------------------------------------
# Применение гибридного разбиения (НОВЫЙ API)
# --------------------------------------------------------------

print("🔧 Настраиваю HybridChunker...")
# Новый API HybridChunker
chunker = HybridChunker(
    chunk_size=8000,  # Вместо max_tokens
    overlap=100       # Перекрытие между фрагментами
)

print("✂️ Разбиваю документ на смысловые фрагменты...")
chunk_iter = chunker.chunk(dl_doc=result.document)
chunks = list(chunk_iter)

print(f"✅ Разбиение завершено!")
print(f"📊 Статистика:")
print(f"   • Всего фрагментов: {len(chunks)}")
print(f"   • Размер фрагмента: до 1024 токенов")

# --------------------------------------------------------------
# Анализ созданных фрагментов
# --------------------------------------------------------------

print("\n" + "="*60)
print("АНАЛИЗ СОЗДАННЫХ ФРАГМЕНТОВ:")
print("="*60)

for i, chunk in enumerate(chunks[:3]):  # Показываем первые 3 фрагмента
    print(f"\n📋 Фрагмент {i+1}:")
    print(f"   • Размер: {len(chunk.text)} символов")
    print(f"   • Заголовки: {chunk.meta.headings if chunk.meta.headings else 'Нет'}")
    print(f"   • Превью: {chunk.text[:200]}...")

if len(chunks) > 3:
    print(f"\n... и еще {len(chunks) - 3} фрагментов")

print(f"\n💾 Общее количество фрагментов готово для эмбеддинга: {len(chunks)}")

# --------------------------------------------------------------
# Функция сохранения чанков в Markdown
# --------------------------------------------------------------

def save_chunks_to_markdown(chunks, filename="chunks_output.md"):
    """
    Сохраняет все чанки в красивый Markdown файл
    
    Args:
        chunks: список чанков от HybridChunker
        filename: имя выходного файла
    """
    with open(filename, "w", encoding="utf-8") as f:
        # Заголовок документа
        f.write("# Анализ фрагментов документа\n\n")
        f.write(f"**Дата создания:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Общее количество фрагментов:** {len(chunks)}\n\n")
        f.write("---\n\n")
        
        # Содержание
        f.write("## Содержание\n\n")
        for i, chunk in enumerate(chunks, 1):
            headings = chunk.meta.headings if chunk.meta.headings else ["Без заголовка"]
            main_heading = headings[0] if headings else f"Фрагмент {i}"
            f.write(f"- [Фрагмент {i}: {main_heading}](#фрагмент-{i})\n")
        f.write("\n---\n\n")
        
        # Детальные фрагменты
        for i, chunk in enumerate(chunks, 1):
            f.write(f"## Фрагмент {i}\n\n")
            
            # Метаданные
            f.write("### 📊 Метаданные\n\n")
            f.write(f"- **Размер текста:** {len(chunk.text)} символов\n")
            
            # Заголовки
            if chunk.meta.headings:
                f.write(f"- **Заголовки:** {' → '.join(chunk.meta.headings)}\n")
            else:
                f.write("- **Заголовки:** Отсутствуют\n")
            
            # Дополнительные метаданные если есть
            if hasattr(chunk.meta, 'page') and chunk.meta.page:
                f.write(f"- **Страница:** {chunk.meta.page}\n")
            
            f.write("\n")
            
            # Содержимое фрагмента
            f.write("### 📝 Содержимое\n\n")
            f.write("```text\n")
            f.write(chunk.text)
            f.write("\n```\n\n")
            
            # Разделитель между фрагментами
            if i < len(chunks):
                f.write("---\n\n")
    
    print(f"📁 Все фрагменты сохранены в файл: {filename}")

# --------------------------------------------------------------
# Сохранение чанков в файл
# --------------------------------------------------------------

print("\n" + "="*60)
print("СОХРАНЕНИЕ ФРАГМЕНТОВ:")
print("="*60)

save_chunks_to_markdown(chunks, "chunks_analysis.md")
print("✅ Готово! Теперь вы можете открыть файл 'chunks_analysis.md' для просмотра всех фрагментов.")