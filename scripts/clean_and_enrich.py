import pandas as pd
import numpy as np
import os

def clean_and_enrich_data(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    
    # 1. Удаление мета-страниц
    df_clean = df[~df['Name'].str.contains('Characters', case=False, na=False)].copy()

    # 2. Строгая нормализация рас под классы OWL
    def normalize_species(s):
        if pd.isna(s): return None
        s = str(s).lower()
        species_list = ['turian', 'asari', 'human', 'krogan', 'salarian', 'quarian', 
                        'geth', 'reaper', 'volus', 'elcor', 'hanar', 'drell', 
                        'batarian', 'vorcha', 'angara', 'kett', 'prothean', 'collector', 'yahg']
        for sp in species_list:
            if sp in s: return sp.title()
        if any(x in s for x in ['synthetic', 'ai', 'vi', 'mech']): return 'Synthetic'
        return s.title()

    df_clean['Species'] = df_clean['Species'].apply(normalize_species)

    # 3. Восстановление фракций на основе лора и титулов (ME1 Timeline)
    def impute_affiliation(row):
        affil = str(row['Affiliation']).lower() if pd.notna(row['Affiliation']) else ''
        title = str(row['Title']).lower() if pd.notna(row['Title']) else ''
        name = str(row['Name']).lower()
        species = str(row['Species']) if pd.notna(row['Species']) else ''
        
        # Эвристика по титулам
        if 'cerberus' in affil or 'cerberus' in title: return 'Cerberus'
        if 'alliance' in affil or 'alliance' in title or 'n7' in title or 'pathfinder' in title: return 'Systems Alliance'
        if 'c-sec' in title or 'c-sec' in affil or 'citadel security' in title: return 'Citadel Security'
        if 'blood pack' in title or 'blood pack' in affil: return 'Blood Pack'
        if 'blue suns' in title or 'blue suns' in affil: return 'Blue Suns'
        if 'eclipse' in title or 'eclipse' in affil: return 'Eclipse'
        if 'spectre' in title or 'spectre' in affil: return 'Citadel Council'
        if 'turian hierarchy' in title or 'turian hierarchy' in affil or 'turian general' in title or 'primarch' in title: return 'Turian Hierarchy'
        if 'stg' in title or 'salarian union' in affil: return 'Salarian Union'
        
        if species == 'Geth':
            return 'Geth Heretics' if 'heretic' in title else 'Geth Consensus'
            
        # Хардкод каноничных фракций для ключевых героев ME1
        lore_dict = {
            'shepard': 'Systems Alliance',
            'garrus vakarian': 'Citadel Security',
            'tali': 'Migrant Fleet',
            'urdnot wrex': 'Blood Pack',
            'saren arterius': 'Citadel Council',
            'david anderson': 'Systems Alliance',
            'steven hackett': 'Systems Alliance',
            'ashley williams': 'Systems Alliance',
            'kaidan alenko': 'Systems Alliance',
            'jeff "joker" moreau': 'Systems Alliance'
        }
        
        for key, val in lore_dict.items():
            if key in name:
                return val
                
        return row['Affiliation'] if pd.notna(row['Affiliation']) else None

    df_clean['Affiliation'] = df_clean.apply(impute_affiliation, axis=1)

    # Замена NaN на пустые строки для корректного импорта в Protégé
    df_clean.replace({np.nan: ''}, inplace=True)
    df_clean.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Dataset enriched! Total instances: {len(df_clean)}")

if __name__ == "__main__":
    clean_and_enrich_data('../data/characters_properties.csv', '../data/MEOntology_Enriched_ABox.csv')