import os
import pandas as pd
from django.core.management.base import BaseCommand
from supplier.models import NUTSRegion  # Altere 'your_app' para o nome do seu app

class Command(BaseCommand):
    help = 'Loads postal code to NUTS mapping data into database'
    
    def handle(self, *args, **options):
        # Caminho para o arquivo CSV
        csv_path = os.path.join(os.path.dirname(__file__), '../../../processed_europe_postal_nuts.csv')
        
        try:
            # Carregar dados em chunks
            chunksize = 10000
            total_rows = 0
            for chunk in pd.read_csv(csv_path, chunksize=chunksize, dtype={'POSTCODE': str}):
                # Preparar objetos para bulk_create
                objs = [
                    NUTSRegion(
                        postal_code=row['POSTCODE'],
                        country_code=row['CNTR_CODE'],
                        nuts0=row['nuts0'],
                        nuts1=row['nuts1'],
                        nuts2=row['nuts2'],
                        nuts3=row['nuts3']
                    )
                    for _, row in chunk.iterrows()
                ]
                
                # Inserir no banco
                NUTSRegion.objects.bulk_create(objs, ignore_conflicts=True)
                total_rows += len(objs)
                self.stdout.write(f'Processed {total_rows} rows...')
            
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {total_rows} records'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV file not found. Please check the path.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))