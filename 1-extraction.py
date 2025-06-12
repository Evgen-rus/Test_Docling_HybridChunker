import os
import pathlib
from docling.document_converter import DocumentConverter

# Настройка локального кэша для HuggingFace моделей
def setup_local_cache():
    """
    Настраивает локальное кэширование HuggingFace моделей.
    Создает необходимые папки и устанавливает переменные окружения.
    """
    cache_dir = pathlib.Path("models_cache").absolute()
    cache_dir.mkdir(exist_ok=True)
    
    # Настройка переменных окружения для HuggingFace
    os.environ["HF_HOME"] = str(cache_dir)
    os.environ["HUGGINGFACE_HUB_CACHE"] = str(cache_dir / "hub")
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
    
    print(f"🔧 Настроен локальный кэш HuggingFace: {cache_dir}")
    return cache_dir

# Инициализация локального кэша перед импортом библиотек
cache_path = setup_local_cache()


#from utils.sitemap import get_sitemap_urls

print("🤖 Инициализация DocumentConverter...")
try:
    converter = DocumentConverter()
    print("✅ DocumentConverter успешно инициализирован!")
except Exception as e:
    print(f"❌ Ошибка инициализации DocumentConverter: {e}")
    print("🔄 Попробуйте запустить скрипт с правами администратора или проверьте интернет-соединение")
    exit(1)

# --------------------------------------------------------------
# Извлечение данных из локального документа пользователя
# --------------------------------------------------------------

print("🚀 Начинаю извлечение данных из документа...")

# Проверка существования файла
pdf_path = "documents/test_simple.pdf"

if not os.path.exists(pdf_path):
    print(f"❌ ОШИБКА: Файл не найден: {pdf_path}")
    print("📁 Проверьте, что файл существует в папке documents/")
    exit(1)

print(f"📄 Файл найден: {pdf_path}")
file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # размер в MB
print(f"📊 Размер файла: {file_size:.2f} MB")

try:
    print("🔄 Начинаю конвертацию PDF...")
    result = converter.convert(pdf_path)
    print("✅ Конвертация PDF завершена успешно!")
    
    print("🔄 Извлекаю содержимое документа...")
    document = result.document
    
    if document is None:
        print("❌ ОШИБКА: Документ не был обработан (document = None)")
        exit(1)
    
    print("🔄 Экспортирую в markdown...")
    markdown_output = document.export_to_markdown()
    
    print("🔄 Экспортирую в JSON...")
    json_output = document.export_to_dict()
    
    print("✅ Документ успешно обработан!")
    print("📄 Размер документа:", len(markdown_output), "символов")
    print("\n" + "="*50)
    print("ПРЕВЬЮ ИЗВЛЕЧЕННОГО ТЕКСТА:")
    print("="*50)
    print(markdown_output[:1000] + "...")
    
except Exception as e:
    print(f"❌ ОШИБКА при обработке документа: {e}")
    print(f"🔧 Тип ошибки: {type(e).__name__}")
    import traceback
    print("📋 Детали ошибки:")
    traceback.print_exc()
    exit(1)

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
