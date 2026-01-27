# preprocess_nuts_data.py
import os
import pandas as pd
import glob

def preprocess_nuts_data(data_dir='data/', output_file='processed_europe_postal_nuts.csv'):
    """
    Processa arquivos CSV de códigos postais NUTS da UE e gera um dataset unificado.
    
    Parâmetros:
        data_dir (str): Diretório com arquivos CSV originais
        output_file (str): Nome do arquivo de saída processado
    
    Formato esperado dos arquivos de entrada:
        'PT1A0';'1069-199'
        'PT1A0';'1070-014'
        ...
    """
    all_data = []
    
    # 1. Coletar todos os arquivos CSV no diretório
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    
    for file_path in csv_files:
        # Extrair código do país do nome do arquivo
        filename = os.path.basename(file_path)
        country_code = filename[7:9].upper()  # Ex: 'IT' de 'pc2024_IT_NUTS-2024_v1.0.csv'
        
        # 2. Ler arquivo CSV
        try:
            df = pd.read_csv(
                file_path, 
                sep=';', 
                dtype=str,
                quotechar="'",
                names=['NUTS_CODE', 'POSTCODE'],
                header=None,
                skiprows=1 
            )
            
            # 3. Limpar dados
            df['NUTS_CODE'] = df['NUTS_CODE'].str.strip("'")
            df['POSTCODE'] = df['POSTCODE'].str.strip("'")
            
            # 4. Extrair níveis hierárquicos
            df['nuts0'] = df['NUTS_CODE'].str[0:2]  # País (NUTS 0)
            df['nuts1'] = df['NUTS_CODE'].str[0:3]  # Grande região (NUTS 1)
            df['nuts2'] = df['NUTS_CODE'].str[0:4]  # Região básica (NUTS 2)
            df['nuts3'] = df['NUTS_CODE']            # Sub-região (NUTS 3)
            
            # 5. Adicionar código do país
            df['CNTR_CODE'] = country_code
            
            all_data.append(df)
            print(f"Processed {filename}: {len(df)} records")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    # 6. Combinar todos os dados
    if all_data:
        combined_df = pd.concat(all_data)
        
        # 7. Salvar resultado
        combined_df.to_csv(output_file, index=False)
        print(f"Saved {len(combined_df)} records to {output_file}")
        return True
    else:
        print("No valid data processed")
        return False

if __name__ == "__main__":
    preprocess_nuts_data()