import pandas as pd

def load_and_process_data(csv_2023_file, csv_2024_file):
    data_2023 = pd.read_csv(csv_2023_file, encoding='utf-8', delimiter=';', on_bad_lines='skip')
    data_2024 = pd.read_csv(csv_2024_file, encoding='utf-8', delimiter=';', on_bad_lines='skip')
    
    data_2023['sintomas'] = data_2023['sintomas'].str.split(',\s*')
    data_2024['sintomas'] = data_2024['sintomas'].str.split(',\s*')
    
    combined_data = pd.concat([data_2023, data_2024])
    
    return combined_data, data_2023, data_2024
