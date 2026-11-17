import requests
import pandas as pd
import time
import os

# Базовый URL API для англоязычной Mass Effect Wiki
API_URL = "https://masseffect.fandom.com/api.php"

def get_pages_in_category(category_name):
    """
    Получает список названий страниц из заданной категории.
    """
    pages = []
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category_name}",
        "cmlimit": "500", # Максимальное количество результатов за один запрос
        "format": "json"
    }
    
    print(f"Fetching pages for category: {category_name}...")

    while True:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        for member in data['query']['categorymembers']:
            # Нас интересуют только основные страницы (ns == 0), исключаем подкатегории и шаблоны
            if member['ns'] == 0:
                pages.append(member['title'])
                
        # Если есть параметр 'continue', значит результатов больше 500, нужна пагинация
        if 'continue' in data:
            params['cmcontinue'] = data['continue']['cmcontinue']
            time.sleep(0.5) # Небольшая пауза, чтобы не спамить API
        else:
            break
            
    return pages

if __name__ == "__main__":
    # Собираем список персонажей
    characters = get_pages_in_category("Characters")
    print(f"Found {len(characters)} characters.")
    
    # Для теста выведем первые 10
    print("Sample characters:", characters[:10])
    
    # Сохраняем черновой список (пока только имена) в CSV
    df = pd.DataFrame({"Name": characters})

    # Получаем абсолютный путь к директории, где лежит сам скрипт (scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Поднимаемся на уровень выше в корень проекта и заходим в data/
    data_dir = os.path.join(script_dir, "..", "data")
    # Формируем итоговый путь к файлу
    output_path = os.path.join(data_dir, "characters_list.csv")

    # Сохраняем файл
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Saved basic character list to {output_path}")