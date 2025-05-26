from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from openai import OpenAI

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
    chunk_size=1024,  # Вместо max_tokens
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