import os
import time
import requests
import pandas as pd
import re

def get_character_properties_api(character_name):
    """
    Получает свойства через официальный MediaWiki API,
    обходя защиту Cloudflare и извлекая данные прямо из вики-кода.
    """
    url = "https://masseffect.fandom.com/api.php"
    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "titles": character_name,
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None, None
            
        data = response.json()
        pages = data['query']['pages']
        
        # Получаем ID страницы (он динамический)
        page_id = list(pages.keys())[0]
        
        # Если страница не найдена
        if page_id == "-1":
            return None, None
            
        # Достаем сырой текст вики-разметки
        rev = pages[page_id]['revisions'][0]
        wikitext = rev.get('slots', {}).get('main', {}).get('*', rev.get('*', ''))
            
        def extract_from_wikitext(keys):
            for key in keys:
                # Ищем строку инфобокса вида: | species = Turian
                pattern = rf"\|\s*{key}\s*=\s*(.+)"
                match = re.search(pattern, wikitext, re.IGNORECASE)
                if match:
                    raw_val = match.group(1).strip()
                    # Очищаем вики-ссылки: [[Turian Hierarchy|Hierarchy]] -> Turian Hierarchy
                    clean_val = re.sub(r'\[\[([^\|\]]+)\|?[^\]]*\]\]', r'\1', raw_val)
                    # Чистим от возможных HTML-тегов
                    clean_val = re.sub(r'<[^>]+>', ' ', clean_val).strip()
                    # Чистим от скобок сносок типа <ref>...</ref>
                    clean_val = re.sub(r'&lt;ref.*?&gt;.*?&lt;/ref&gt;', '', clean_val)
                    return clean_val
            return None
            
        species = extract_from_wikitext(['species', 'race'])
        affiliation = extract_from_wikitext(['affiliation', 'faction', 'organizations', 'organization'])
        title = extract_from_wikitext(['class', 'title', 'position'])
        
        return species, affiliation, title
        
    except Exception as e:
        print(f"Error parsing {character_name}: {e}")
        return None, None

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "..", "data", "characters_list.csv")
    output_path = os.path.join(script_dir, "..", "data", "characters_properties.csv")
    
    df = pd.read_csv(input_path)
    
    # df = df.head(10) 
    
    print(f"Starting API parsing for {len(df)} characters...")
    
    species_list = []
    affiliation_list = []
    title_list = [] 
    
    for index, row in df.iterrows():
        name = row['Name']
        
        species, affiliation, title = get_character_properties_api(name)
        
        print(f"[{index + 1}/{len(df)}] {name} -> Species: {species} | Affiliation: {affiliation} | Title: {title}")
        
        species_list.append(species)
        affiliation_list.append(affiliation)
        title_list.append(title) # Сохраняем должность
        
        time.sleep(0.3)
        
    df['Species'] = species_list
    df['Affiliation'] = affiliation_list
    df['Title'] = title_list
    
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nDone! Saved properties to {output_path}")