import pandas as pd
import numpy as np

def msg_continuar():
    print('Presione enter para continuar')
    input()

#*explorar los datos de los df y los muestra
def explorar_df(df) -> None:
    print('Muestra de datos')
    print(df.head())
    print('\nFormato del dataframe')
    print(df.shape)
    print('\nBúsqueda de valores nulos por columna')
    print(df.isnull().sum())
    print('\nFormato de los datos por columna')
    print(df.dtypes)

#*Chekeo de valores null en el df
def check_null_values(df):
  if df.isnull().sum().values.sum() >0:
      print('Existen valores NaN\n limpiando..')
      df = limpiar_nan(df)#quita los NaN
  print('No existen valores NaN')
  
  return df
      
#*transforma los valores de la col distributors para que se presenten como int
def transformar_valor(valor):
    if valor < 2000:
        return valor
    return valor/10



#*rellena los NaN con 0
def limpiar_nan(df):
    return df.fillna(0)


#*castea una columna a int
def cast_int(df):
    return df.astype(str).str.replace('.', '',).astype(int).apply(transformar_valor).astype(int)


#*limpiar simbolos y reemplazar otros
def limpiar_simbolos(df):
    return df.replace('$', '',).replace('.', '',).replace(',', '.',) 

#*elimina columnas innecesarias o vacias
def del_columnas(df,lista_col):
  for col in lista_col:
    df.drop(col, axis=1, inplace=True)
  return df

#*Crea un configuracion inicial de como se deben mostrar los datos del df
def setup_df():
    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.float_format', '{:.2f}'.format)
    

setup_df() #aplicar config

#*Lista con los nombres de las hojas de la base de datos
HOJAS = ['sales_in_paraguay','distributors_profiles','exports_to_paraguay','locations_profiles', ]

#*id de la planilla que contiene todas las hojas
id_planilla = '1_llWFVuc66VgauNo1EzNEpAg55nXHgkp4CNTxpbDETk'

#*Lista que guarda todas las urls correspondientes a la base de datos para poder ser accedidas
URLs = [f'https://docs.google.com/spreadsheets/d/{id_planilla}/gviz/tq?tqx=out:csv&sheet={hoja}' for hoja in HOJAS]

#*creacion de los dataframes
dataframes = [pd.read_csv(url) for url in URLs]

#*desempaquetado de los df
df_sales_in_paraguay, df_distributors_profiles, df_exports_to_paraguay, df_locations_profiles  = dataframes



# #! Limpieza df_sales_in_paraguay
explorar_df(df=df_sales_in_paraguay)

 #eliminar columnas innecesarias
df_sales_in_paraguay = check_null_values(df_sales_in_paraguay) #chekear valores NaN
df_sales_in_paraguay = df_sales_in_paraguay.iloc[:-1].replace('$0.00', 0)
for columna in df_sales_in_paraguay.columns:
    if columna == 'distributor':
       df_sales_in_paraguay['distributor'] = cast_int(df_sales_in_paraguay['distributor'])   
    else:  
         df_sales_in_paraguay[columna] = df_sales_in_paraguay[columna].apply(limpiar_simbolos)
         df_sales_in_paraguay = df_sales_in_paraguay[columna].astype(float)
      
explorar_df(df=df_sales_in_paraguay)


msg_continuar()

##!Limpieza df_exports_to_paraguay

explorar_df(df=df_exports_to_paraguay)

df_exports_to_paraguay = del_columnas(df_exports_to_paraguay, ['Columnas','Unnamed: 13','Unnamed: 14']) #eliminar columnas innecesarias
df_exports_to_paraguay = check_null_values(df_exports_to_paraguay) #chekear valores NaN
    
for columna in df_exports_to_paraguay.columns:
    if columna == 'distributor':
        df_exports_to_paraguay['distributor'] = cast_int(df_exports_to_paraguay['distributor']) #transformar a int 'distributor'
    else:
            df_exports_to_paraguay[columna] = df_exports_to_paraguay[columna].apply(limpiar_simbolos) #limpieza de simbolos inecesarios
            df_exports_to_paraguay[columna] = df_exports_to_paraguay[columna].astype(float) #transforma a float todos los datos


explorar_df(df=df_exports_to_paraguay)

