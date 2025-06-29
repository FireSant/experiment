import pandas as pd
import openpyxl 

# Cargar el archivo adult.csv en un DataFrame
df = pd.read_csv('adult.csv')

# Exportar el DataFrame a un archivo Excel
df.to_excel('output_adult_data.xlsx', index=False)

print("Datos exportados a 'output_adult_data.xlsx'")