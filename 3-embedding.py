from typing import List

import lancedb
from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
client = OpenAI()

print("🚀 Создаем эмбеддинги для документа...")

# --------------------------------------------------------------
# Extract the data
# --------------------------------------------------------------

converter = DocumentConverter()
result = converter.convert("documents/ЛОГИКА_ПРОДАЖИ_ТЕСТОВОГО_ПЕРИОДА_ЛИДГЕНБЮРО.md")

# --------------------------------------------------------------
# Apply hybrid chunking (НОВЫЙ API)
# --------------------------------------------------------------

chunker = HybridChunker(
    chunk_size=1024,  # Вместо max_tokens
    overlap=100       # Перекрытие
)

chunk_iter = chunker.chunk(dl_doc=result.document)
chunks = list(chunk_iter)
print(f"✂️ Создано {len(chunks)} фрагментов для эмбеддинга")

# --------------------------------------------------------------
# Create a LanceDB database and table
# --------------------------------------------------------------

# Create a LanceDB database
db = lancedb.connect("data/lancedb")

# Get the OpenAI embedding function
func = get_registry().get("openai").create(name="text-embedding-3-small")

# Define a simplified metadata schema
class ChunkMetadata(LanceModel):
    """
    You must order the fields in alphabetical order.
    This is a requirement of the Pydantic implementation.
    """

    filename: str
    title: str

# Define the main Schema
class Chunks(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()  # type: ignore
    metadata: ChunkMetadata

table = db.create_table("docling", schema=Chunks, mode="overwrite")

# --------------------------------------------------------------
# Prepare the chunks for the table
# --------------------------------------------------------------

# Create table with processed chunks - упрощенная структура метаданных
processed_chunks = []

for chunk in chunks:
    # Безопасное извлечение filename
    filename = "unknown"
    if hasattr(chunk, 'meta') and chunk.meta:
        if hasattr(chunk.meta, 'origin') and chunk.meta.origin:
            if hasattr(chunk.meta.origin, 'filename') and chunk.meta.origin.filename:
                filename = chunk.meta.origin.filename
    
    # Безопасное извлечение title  
    title = "Untitled"
    if hasattr(chunk, 'meta') and chunk.meta:
        if hasattr(chunk.meta, 'headings') and chunk.meta.headings:
            if len(chunk.meta.headings) > 0:
                title = chunk.meta.headings[0]
    
    processed_chunk = {
        "text": chunk.text,
        "metadata": {
            "filename": filename,
            "title": title,
        },
    }
    processed_chunks.append(processed_chunk)

print(f"📦 Подготовлено {len(processed_chunks)} фрагментов для индексации")

# --------------------------------------------------------------
# Add the chunks to the table (automatically embeds the text)
# --------------------------------------------------------------

table.add(processed_chunks)
print("💾 Эмбеддинги сохранены в LanceDB!")
print(f"📊 Всего записей в базе: {table.count_rows()}")

# --------------------------------------------------------------
# Load the table
# --------------------------------------------------------------

print("\n📋 Пример данных из таблицы:")
sample = table.to_pandas().head(3)
for idx, row in sample.iterrows():
    print(f"  • Фрагмент {idx + 1}: {row['text'][:100]}...")
    print(f"    Метаданные: {row['metadata']}")

print(f"\n✅ Готово! Всего записей: {table.count_rows()}")
