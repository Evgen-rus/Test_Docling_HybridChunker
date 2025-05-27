import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from docling.document_converter import DocumentConverter
from utils.sitemap import get_sitemap_urls

converter = DocumentConverter()

# --------------------------------------------------------------
# Извлечение данных из локального документа пользователя
# --------------------------------------------------------------

print("🚀 Начинаю извлечение данных из документа...")
result = converter.convert("documents/A1209_инструкция.pdf")

document = result.document
markdown_output = document.export_to_markdown()
json_output = document.export_to_dict()

print("✅ Документ успешно обработан!")
print("📄 Размер документа:", len(markdown_output), "символов")
print("\n" + "="*50)
print("ПРЕВЬЮ ИЗВЛЕЧЕННОГО ТЕКСТА:")
print("="*50)
print(markdown_output[:1000] + "...")

# --------------------------------------------------------------
# Сохранение результатов для проверки
# --------------------------------------------------------------

with open("extracted_content.md", "w", encoding="utf-8") as f:
    f.write(markdown_output)
    
print("\n📁 Результат сохранен в файл: extracted_content.md")

# --------------------------------------------------------------
# Оригинальные примеры (закомментированы)
# --------------------------------------------------------------

# # Basic PDF extraction
# result = converter.convert("https://arxiv.org/pdf/2408.09869")
# document = result.document
# markdown_output = document.export_to_markdown()
# json_output = document.export_to_dict()
# print(markdown_output)

# # Basic HTML extraction
# result = converter.convert("https://ds4sd.github.io/docling/")
# document = result.document
# markdown_output = document.export_to_markdown()
# print(markdown_output)

# # Scrape multiple pages using the sitemap
# sitemap_urls = get_sitemap_urls("https://ds4sd.github.io/docling/")
# conv_results_iter = converter.convert_all(sitemap_urls)
# docs = []
# for result in conv_results_iter:
#     if result.document:
#         document = result.document
#         docs.append(document)
