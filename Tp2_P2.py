import pandas as pd
import numpy as np



#castear a enteros
def cast_int(value):
   # return int(value * 1000) if value < 100 else int(value)
   return value

def cast_int2(value):
    value = str(value).replace('.', '')

    return  int(value)

#rellena los NaN con -1
def limpiar_nan(df):

    return df.fillna(-1)

#castear a float
def cast_float(value):
    return float(value)

#limpiar simbolos y reemplazar otros
def limpiar_simbolos(col):

    col = col.str.replace(r'\$', '', regex=True)
    col = col.str.replace(r'\.', '', regex=True)  # Eliminar puntos
    col = col.str.replace(r',', '.', regex=False)  # Reemplazar comas por puntos
    return col

#elimina columnas innecesarias o vacias
def del_columnas(df,lista_col):
  for col in lista_col:
    df.drop(col, axis=1, inplace=True)
  return df


def setup_df():
    # Configuracion de como mostrar los datos del DataFrame
    pd.set_option('display.max_rows', None)
    pd.set_option('display.float_format', '{:.2f}'.format)
    


# Configuracion de como mostrar los datos del DataFrame
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', '{:.2f}'.format)

# diccionario con nombre de las hojas y sus respectivos IDs
ID_planillas = {
    'sales_in_paraguay'    : '1C79auNWTtNjRulOWZ6YFmZylqRmWy4FitMcsvsxDSLU',

    'locations_profiles'   : '1hqk0GXhwqTJ8pUPHhyxwh00tCN_4W9hnGxRu4bMag9Y',

    'exports_to_paraguay'  : '1hqyesVMiDwyM-5aUlIPUrIj9SBCC_O7yRq_qcAyMgR8',

    'distributors_profiles': '1tngxaAfsgZnwWFYwL-elH8gXJmvYdoRL2sDh4jiZxBE' ,
}

# Lista que guarda todas las urls correspondientes a la base de datos para poder ser accedidas
URLs = [f'https://docs.google.com/spreadsheets/d/{id_planilla}/gviz/tq?tqx=out:csv&sheet={hoja}' for hoja, id_planilla in ID_planillas.items()]

#creacion de los dataframes
dataframes = [pd.read_csv(url) for url in URLs]

# desempaquetado de los df
df_sales_in_paraguay, df_locations_profiles, df_exports_to_paraguay, df_distributors_profiles = dataframes




# Limpieza df_sales_in_paraguay
df_sales_in_paraguay = limpiar_nan(df_sales_in_paraguay) #quita los NaN


for columna in df_sales_in_paraguay.columns:

  if columna != 'distributor':
    df_sales_in_paraguay[columna] = limpiar_simbolos(df_sales_in_paraguay[columna])
    df_sales_in_paraguay[columna] = df_sales_in_paraguay[columna].apply(cast_float)

  df_sales_in_paraguay[columna] = df_sales_in_paraguay[columna].apply(cast_int) # castea a int




 #Limpieza df_exports_to_paraguay
df_exports_to_paraguay = limpiar_nan(df_exports_to_paraguay)#quita los NaN
df_exports_to_paraguay = del_columnas(df_exports_to_paraguay, ['Columnas','Unnamed: 13','Unnamed: 14']) #eliminar columnas innecesarias

for columna in df_exports_to_paraguay.columns:
  if columna != 'distributor':
    df_exports_to_paraguay[columna] = limpiar_simbolos(df_exports_to_paraguay[columna])
    df_exports_to_paraguay[columna] = df_exports_to_paraguay[columna].apply(cast_float)
  df_exports_to_paraguay[columna] = df_exports_to_paraguay[columna].apply(cast_int2) #!!! TRATAR DE ELIMINAR EL PUNTO Y CASTEAR A INT

setup_df()

