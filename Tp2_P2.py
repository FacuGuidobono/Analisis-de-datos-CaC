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
        df = limpiar_nan(df)#quita los NaN
    else:
        pass
    return df

#*buscar columnas identicas (duplicadas)

def search_duplicates(df):
    
    columns = df.columns
# Inicializar una lista para almacenar las columnas que son exactamente iguales
    duplicates = []
    # Comparar todas las columnas entre sí
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            if df[columns[i]].equals(df[columns[j]]):
                duplicates.append((columns[i], columns[j]))

    print("Pares de columnas que son exactamente iguales:", len(duplicates))
    return duplicates

#*transforma los valores de la col distributors para que se presenten como int
def transformar_valor(valor):
    if valor < 2000 and valor > 999:
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
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)
        else:
           pass
    return df

#*Crea un configuracion inicial de como se deben mostrar los datos del df
def setup_df():
    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.float_format', '{:.2f}'.format)
    
#!----------------------------------------------------------------------------------------
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

#?solo usar sales,export & distributors

#!----------------------------------------------------------------------------------------
#! Limpieza df_sales_in_paraguay



df_sales_in_paraguay = check_null_values(df_sales_in_paraguay)#chekear valores NaN
df_sales_in_paraguay = df_sales_in_paraguay.drop(df_sales_in_paraguay.index[-1]) #elimina la ultia fila del df

a = search_duplicates(df_sales_in_paraguay)
if len(a) != 0:
    df_sales_in_paraguay = del_columnas(df=df_sales_in_paraguay,lista_col=a) #eliminar columnas innecesarias

for columna in df_sales_in_paraguay.columns: 
    if columna == 'distributor':
        df_sales_in_paraguay['distributor'] = cast_int(df_sales_in_paraguay['distributor'])   
    else:  
        df_sales_in_paraguay[columna] = df_sales_in_paraguay[columna].apply(limpiar_simbolos)
        df_sales_in_paraguay[columna]= df_sales_in_paraguay[columna].astype(float)
        

#!----------------------------------------------------------------------------------------
#!Limpieza df_distributors_profiles



a = search_duplicates(df_distributors_profiles)
if len(a) != 0:
    df_distributors_profiles = del_columnas(df=df_distributors_profiles, lista_col=a) #eliminar columnas innecesarias

df_distributors_profiles = check_null_values(df_distributors_profiles) #chekear valores NaN
df_distributors_profiles['id'] = cast_int(df_distributors_profiles['id']) #transformar a int 'distributor'

for columna in df_distributors_profiles.columns:
    df_distributors_profiles = df_distributors_profiles.drop(df_distributors_profiles.index[df_distributors_profiles[columna] == 0])


#!----------------------------------------------------------------------------------------
##!Limpieza df_exports_to_paraguay


a = search_duplicates(df_sales_in_paraguay)

if len(a) != 0:
    a = a + ['Columnas','Unnamed: 13','Unnamed: 14']
    df_sales_in_paraguay = del_columnas(df=df_sales_in_paraguay,lista_col=a)
else:
    df_exports_to_paraguay = del_columnas(df_exports_to_paraguay, ['Columnas','Unnamed: 13','Unnamed: 14']) #eliminar columnas innecesarias

df_exports_to_paraguay = check_null_values(df_exports_to_paraguay) #chekear valores NaN
    
for columna in df_exports_to_paraguay.columns:
    if columna == 'distributor':
        df_exports_to_paraguay['distributor'] = cast_int(df_exports_to_paraguay['distributor']) #transformar a int 'distributor'
    else:
            df_exports_to_paraguay[columna] = df_exports_to_paraguay[columna].apply(limpiar_simbolos) #limpieza de simbolos inecesarios
            df_exports_to_paraguay[columna] = df_exports_to_paraguay[columna].astype(float) #transforma a float todos los datos




#!----------------------------------------------------------------------------------------
#!Limpieza df_locations_profiles

a = search_duplicates(df_locations_profiles)
if len(a) != 0:
    df_locations_profiles = del_columnas(df=df_locations_profiles, lista_col=a) #eliminar columnas innecesarias
unnamed_columns = [f'Unnamed: {i}' for i in range(5, 26)] #
df_locations_profiles = del_columnas(df=df_locations_profiles, lista_col=unnamed_columns)
df_locations_profiles = check_null_values(df_locations_profiles) #chekear valores NaN
df_locations_profiles['PYid'] = cast_int(df_locations_profiles['PYid']) #transformar a int 'distributor'
df_locations_profiles['id']  = cast_int(df_locations_profiles['id']) #transformar a int 'distributor'


#!----------------------------------------------------------------------------------------
#!ANALISIS 

#?VENTAS
#ordeno el df por distribuidor y los ordeno de forma asc
df_sales_in_paraguay = df_sales_in_paraguay.sort_values(by='distributor', ascending=True)

#sumo todos los valores despues de 'distributor' y los ordeno de forma asc
total_sales = df_sales_in_paraguay.iloc[:,1:].sum().sort_values(ascending=True) 

#creo un nuevo df para el total de ventas correspondiente a cada rubro
total_sales = pd.DataFrame(total_sales/1000000, columns=['Ventas Totales (Millones de $)'])

print(total_sales)

#?EXPORTACIONES
#ordeno el df por distribuidor y los ordeno de forma asc
df_exports_to_paraguay = df_exports_to_paraguay.sort_values(by='distributor', ascending=True)

#sumo todos los valores despues de 'distributor' y los ordeno de forma desc
total_exports = df_exports_to_paraguay.iloc[:,1:].sum().sort_values(ascending=False)

#creo un nuevo df para el total de ventas correspondiente a cada rubro
total_exports = pd.DataFrame(total_exports/1000000, columns=['Exportaciones Totales (Millones de $)'])

print(total_exports)

