import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#*explorar los datos de los df y los muestra
def explorar_df(df) -> None:
    print('Muestra de datos')
    df.head()
    print('\nFormato del dataframe')
    df.shape
    print('\nBúsqueda de valores nulos por columna')
    df.isnull().sum()
    print('\nFormato de los datos por columna')
    df.dtypes

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

#buscar filas identicas (duplicadas)
def search_duplicates_row(df):
    
    if df.duplicated().sum() != 0 :
        print( f'Pares de filas que son exactamente iguales: {df.duplicated().sum()}' )

        df = df.drop_duplicates(subset=df.columns, keep='first', inplace=True)
    else:
        print( f'Pares de filas que son exactamente iguales: 0' )
        return
    return df

#*transforma los valores de la col distributors para que se presenten como int
def transformar_valor(valor):
    if valor < 2000 and valor > 999:
        return valor
    return valor/10


def transformar_valor2(valor):
    if valor < 2 and valor > 1 :
        return valor*1000
    return valor


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

#!--------------------------------------------------------------------------------------
#! Inspeccion preeliminar

#? VENTAS
explorar_df(df_sales_in_paraguay)

#? EXPORTACIONES
explorar_df(df_exports_to_paraguay)

#? DISTRIBUIDORES
explorar_df(df_distributors_profiles)


#!----------------------------------------------------------------------------------------
#! Limpieza VENTAS



df_sales_in_paraguay = check_null_values(df_sales_in_paraguay)#chekear valores NaN
df_sales_in_paraguay = df_sales_in_paraguay.drop(df_sales_in_paraguay.index[-1]) #elimina la ultia fila del df

a = search_duplicates(df_sales_in_paraguay)
if len(a) != 0:
    df_sales_in_paraguay = del_columnas(df=df_sales_in_paraguay,lista_col=a) #eliminar columnas innecesarias

search_duplicates_row(df_sales_in_paraguay) # buscar filas duplicadas y eliminarlas

for columna in df_sales_in_paraguay.columns:
    if columna == 'distributor':
        df_sales_in_paraguay[columna] = df_sales_in_paraguay[columna].apply(transformar_valor2).astype(int)  
    else:
        df_sales_in_paraguay[columna] = df_sales_in_paraguay[columna].apply(limpiar_simbolos)
        df_sales_in_paraguay[columna]= df_sales_in_paraguay[columna].astype(float)


#!----------------------------------------------------------------------------------------
##!Limpieza EXPORTACIONES

a = search_duplicates(df_sales_in_paraguay)

if len(a) != 0:
    a = a + ['Columnas','Unnamed: 13','Unnamed: 14']
    df_sales_in_paraguay = del_columnas(df=df_sales_in_paraguay,lista_col=a)
else:
    df_exports_to_paraguay = del_columnas(df_exports_to_paraguay, ['Columnas','Unnamed: 13','Unnamed: 14']) #eliminar columnas innecesarias

df_exports_to_paraguay = check_null_values(df_exports_to_paraguay) #chekear valores NaN
search_duplicates_row(df_exports_to_paraguay) # buscar filas duplicadas y eliminarlas
for columna in df_exports_to_paraguay.columns:
    if columna == 'distributor':
        df_exports_to_paraguay[columna] = df_exports_to_paraguay[columna].apply(transformar_valor2).astype(int) #transformar a int 'distributor'
        
    else:
            df_exports_to_paraguay[columna] = df_exports_to_paraguay[columna].apply(limpiar_simbolos) #limpieza de simbolos inecesarios
            df_exports_to_paraguay[columna] = df_exports_to_paraguay[columna].astype(float) #transforma a float todos los datos


#!----------------------------------------------------------------------------------------
#!Limpieza DISTRIBUIDORES



a = search_duplicates(df_distributors_profiles)
if len(a) != 0:
    df_distributors_profiles = del_columnas(df=df_distributors_profiles, lista_col=a) #eliminar columnas innecesarias
df_distributors_profiles = check_null_values(df_distributors_profiles) #chekear valores NaN

search_duplicates_row(df_distributors_profiles) # buscar filas duplicadas y eliminarlas

df_distributors_profiles['id'] = df_distributors_profiles['id'].apply(transformar_valor2).astype(int)#transformar a int 'id'
df_distributors_profiles.loc[36, 'id'] = 1017
for columna in df_distributors_profiles.columns:
    df_distributors_profiles = df_distributors_profiles.drop(df_distributors_profiles.index[df_distributors_profiles[columna] == 0])



# #!----------------------------------------------------------------------------------------
# #!Limpieza df_locations_profiles

# a = search_duplicates(df_locations_profiles)
# if len(a) != 0:
#     df_locations_profiles = del_columnas(df=df_locations_profiles, lista_col=a) #eliminar columnas innecesarias
    
# df_locations_profiles = check_null_values(df_locations_profiles) #chekear valores NaN
# unnamed_columns = [f'Unnamed: {i}' for i in range(5, 26)] #elimina todas las columnas que no tengan nombre
# df_locations_profiles = del_columnas(df=df_locations_profiles, lista_col=unnamed_columns)



# df_locations_profiles['PYid'] = cast_int(df_locations_profiles['PYid']) #transformar a int 'distributor'
# df_locations_profiles['id']  = cast_int(df_locations_profiles['id']) #transformar a int 'distributor'


#!----------------------------------------------------------------------------------------
#!ANALISIS 

#* Bajas ventas de acero y ladrillos
#* Realizamos una comparacion entre Exportación y Ventas.

#?VENTAS
#ordeno el df por distribuidor y los ordeno de forma asc
df_sales_in_paraguay = df_sales_in_paraguay.sort_values(by='distributor', ascending=True)

#sumo todos los valores despues de 'distributor' y los ordeno de forma asc
total_sales = df_sales_in_paraguay.iloc[:,1:].sum().sort_values(ascending=False)

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

#?COMBINACION LOS DF

total_combinados = pd.merge(total_exports.reset_index(), total_sales.reset_index(), on='index')

total_combinados.set_index('index', inplace=True)

print(total_combinados)

#? add ratio/ventas ventas sobre las exportaciones (proporcion)

total_combinados['ratio Ventas/Exportaciones'] = total_combinados['Ventas Totales (Millones de $)'] / total_combinados['Exportaciones Totales (Millones de $)']
print(total_combinados) 

#!----------------------------------------------------------------------------------------
#!ANALISIS VISUAL


#? Grafico de barras config
fig,ax = plt.subplots(nrows=2, ncols=1 ,figsize=(10, 10))


#?GRAFICO DE BARRAS PARA VENTAS ROW0
sns.barplot(x=total_sales.index, y= total_sales['Ventas Totales (Millones de $)'], ax=ax[0])
ax[0].set_title('Ventas totales por producto') # titulo del grafico
ax[0].set_xlabel('Productos') # nombre del eje x
ax[0].set_ylabel('Suma Total (Millones de $)') # nombre del eje Y
ax[0].tick_params(axis='x', rotation=45) # ver la etiquetas en eje x

#?GRAFICO DE BARRAS PARA EXPORTACIONES ROW1
sns.barplot(x=total_exports.index, y= total_exports['Exportaciones Totales (Millones de $)'], ax=ax[1])
ax[1].set_title('Exportaciones totales por producto') # titulo del grafico
ax[1].set_xlabel('Productos') # nombre del eje x
ax[1].set_ylabel('Suma Total (Millones de $)') # nombre del eje Y
ax[1].tick_params(axis='x', rotation=45) # ver la etiquetas en eje x

plt.tight_layout()
plt.show()



#?GRAFICO PRORCION DE VENTAS/EXPORTACION
plt.figure(figsize=(10,6))
sns.barplot(x=total_combinados.index, y= 'ratio Ventas/Exportaciones', data=total_combinados)
plt.title('Ratio Ventas/Exportaciones')
plt.xlabel('Productos')
plt.ylabel('Ratio')
plt.xticks(rotation=45)

for index, value in enumerate(total_combinados['ratio Ventas/Exportaciones']):
    plt.text(index, value + 0.02, f'{value:.2f}', ha='center', va='bottom', fontsize= 9)

plt.tight_layout()
plt.show()


#?GRAFICO DE BARRAS COMPARACION VENTAS TOTALES Y EXPORTACIONES TOTALES

plt.figure(figsize=(10,6))
plt.plot(total_combinados.index, total_combinados['Ventas Totales (Millones de $)'], marker='o' , linestyle = '-', color='magenta', label = 'Ventas Totales')
plt.plot(total_combinados.index, total_combinados['Exportaciones Totales (Millones de $)'], marker='s',linestyle = '-', color = 'red', label = 'Exportaciones Totales')

plt.title('Comparacion de Ventas Totales y Exportaciones Totales por Indice')
plt.xlabel('Indice')
plt.ylabel('Suma Total (Millones de $) ')
plt.xticks(rotation=90)
plt.legend()

plt.tight_layout()
plt.show()


#?GRAFICO COMPARACION DE VENTAS TOTALES Y EXPORTACIONES TOTALES POR PRODUCTO

plt.figure(figsize=(10,6))

bar_width = 0.35
indices = range(len(total_combinados))

plt.bar(indices, total_combinados['Ventas Totales (Millones de $)'], width=bar_width, label='Ventas Totales', color='magenta', alpha=0.7)
plt.bar([i + bar_width for i in indices], total_combinados['Exportaciones Totales (Millones de $)'], width=bar_width, label='Exportaciones Totales', color='red')

plt.xlabel('Productos')
plt.ylabel('Suma Total (Millones de $)')
plt.title('COMPARACION DE VENTAS TOTALES Y EXPORTACIONES TOTALES POR PRODUCTO')
plt.xticks([i + bar_width / 2 for i in indices], total_combinados.index,rotation=90)
plt.legend()
plt.tight_layout()
plt.show()
