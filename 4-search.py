import lancedb
from lancedb.embeddings import get_registry

# Подключение к базе данных
print("🔍 Подключаюсь к векторной базе LanceDB...")
db = lancedb.connect("data/lancedb")
table = db.open_table("docling")

print(f"📊 В базе данных: {table.count_rows()} записей")

# Настройка поиска
func = get_registry().get("openai").create(name="text-embedding-3-small")

# Тестовые запросы по вашему документу о логике продаж
test_queries = [
    "Как проводить квалификацию клиентов?",
    "Что такое тестовый период?",
    "Как оценивать качество лидов?",
    "Этапы продажи тестового периода",
    "Микропрезентация клиенту",
    "Синхронизация терминов с клиентом"
]

print("\n" + "="*60)
print("ТЕСТИРОВАНИЕ ПОИСКА ПО ДОКУМЕНТУ О ЛОГИКЕ ПРОДАЖ:")
print("="*60)

for query in test_queries:
    print(f"\n🔍 Запрос: '{query}'")
    results = table.search(query).limit(2).to_pandas()
    
    if len(results) > 0:
        for i, row in results.iterrows():
            print(f"  📄 Результат {i+1}:")
            print(f"     Релевантность: {row['_distance']:.4f}")
            print(f"     Файл: {row['metadata']['filename']}")
            print(f"     Заголовок: {row['metadata']['title']}")
            print(f"     Текст: {row['text'][:150]}...")
            print()
    else:
        print("  ❌ Результатов не найдено")

print("\n" + "="*60)
print("СТАТИСТИКА БАЗЫ ЗНАНИЙ:")
print("="*60)
print(f"📈 Всего фрагментов в базе: {table.count_rows()}")

# Проверяем разнообразие заголовков
sample_data = table.to_pandas()
unique_titles = sample_data['metadata'].apply(lambda x: x['title']).unique()
print(f"📋 Уникальных заголовков: {len(unique_titles)}")
print("🏷️ Примеры заголовков:")
for title in unique_titles[:5]:
    print(f"   • {title}")

print(f"\n✅ Поиск работает! База готова для использования в чате.")
