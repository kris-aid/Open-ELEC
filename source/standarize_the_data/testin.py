

import os
import pandas as pd
import numpy as np
import re
import sys
import shutil
import unidecode

# Recuperar todas los diccionarios de dignidades de las elecciones y colocarlos en un dataframe

input_folder = "data_csv"

def recuperar_dignidades(input_folder):
    '''
    Recupera todas los diccionarios de dignidades de las elecciones y coloca los en un dataframe
    Se cambian los nombres de las columnas para que no tengan caracteres especiales
    Paramaters
    ----------
        - input_folder: str 
            path al directorio que contiene los archivos .csv
    
    Returns
    -------
        - df_dignidades: DataFrame
            DataFrame con los códigos de dignidades de las elecciones
    
    Examples
    --------
    recuperar_dignidades("data_csv")
         
    '''
    # Crear un DataFrame vacío
    df_dignidades = pd.DataFrame()
    # Listar todos los archivos en el directorio de entrada y sus subdirectorios
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith("dignidades"):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #Los nombres y ambitos de las dignidades están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in ["DIGNIDAD_NOMBRE", "DIGNIDAD_AMBITO"] else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in ["DIGNIDAD_NOMBRE", "DIGNIDAD_AMBITO"] else x)
                    
                    
                    #añadir el año de la elección al DataFrame
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_dignidades = pd.concat([df_dignidades, df])
    return df_dignidades


# Ahora vamos a crear un data frame con el nombre de la DIGNIDAD_NOMBRE y ámbito geográfico.
# Y se van a crear columnas para cada año con el código que le corresponde a esa DIGNIDAD_NOMBRE en ese año.
# Si no hay código para esa DIGNIDAD_NOMBRE en ese año, se va a colocar un NaN
#comprobar si la DIGNIDAD_NOMBRE ya está en el dataframe y si no está, agregarla.
# Si la DIGNIDAD_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
# Si la DIGNIDAD_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección

def crear_df_dignidades(df_dignidades):
    '''
    Crea un data frame con el nombre de la DIGNIDAD_NOMBRE y ámbito geográfico.
    Y se van a crear columnas para cada año con el código que le corresponde a esa DIGNIDAD_NOMBRE en ese año.
    Si no hay código para esa DIGNIDAD_NOMBRE en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_dignidades: DataFrame
            DataFrame con los códigos de dignidades de las elecciones
    
    Returns
    -------
        - df_dignidades_std: DataFrame
            DataFrame con el nombre de la DIGNIDAD_NOMBRE y ámbito geográfico y columnas para cada año con el código que le corresponde a esa DIGNIDAD_NOMBRE en ese año
    
    Examples
    --------
    crear_df_dignidades(df_dignidades)
         
    '''
    # Crear un DataFrame vacío
    df_dignidades_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_dignidades.iterrows():
        # Revisar si la DIGNIDAD_NOMBRE ya está en el dataframe
        if row["DIGNIDAD_NOMBRE"] not in df_dignidades_std.index:
            # Si la DIGNIDAD_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_dignidades_std.loc[row["DIGNIDAD_NOMBRE"], "DIGNIDAD_AMBITO"] = row["DIGNIDAD_AMBITO"]
            df_dignidades_std.loc[row["DIGNIDAD_NOMBRE"], row["ANIO"]] = row["DIGNIDAD_CODIGO"]
        else:
            # Si la DIGNIDAD_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_dignidades_std.loc[row["DIGNIDAD_NOMBRE"], row["ANIO"]] = row["DIGNIDAD_CODIGO"]
    
    # Colocar las columnas de los años en orden
    df_dignidades_std = df_dignidades_std.reindex(sorted(df_dignidades_std.columns), axis=1)
    # Colocar las filas en orden
    df_dignidades_std = df_dignidades_std.sort_index()
    return df_dignidades_std



def recuperar_provincias(input_folder):

    '''
        Recupera todas los diccionarios de provincias de las elecciones y coloca los en un dataframe
        Se cambian las columnas para que no tengan caracteres especiales
        
        Paramaters
        ----------
            - input_folder: str 
                path al directorio que contiene los archivos .csv
        
        Returns
        -------
            - df_provincias: DataFrame
                DataFrame con los códigos de provincias de las elecciones
        
        Examples
        --------
        recuperar_provincias("data_csv")
             
        '''
    # Crear un DataFrame vacío
    df_provincias = pd.DataFrame()
    #De la carpeta, buscar el archivo que empieza con "provincias"
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith("provincias"):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #Los nombres de Provincias están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in ["PROVINCIA_NOMBRE"] else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in ["PROVINCIA_NOMBRE"] else x)
                    
                    #añadir el año de la elección al DataFrame
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_provincias = pd.concat([df_provincias, df])
    return df_provincias

def crear_df_provincias(df_provincias):
    '''
    Crea un data frame con el nombre de la PROVINCIA_NOMBRE y columnas para cada año con el código que le corresponde a esa PROVINCIA_NOMBRE en ese año.
    Si no hay código para esa PROVINCIA_NOMBRE en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_provincias: DataFrame
            DataFrame con los códigos de provincias de las elecciones
    
    Returns
    -------
        - df_provincias_std: DataFrame
            DataFrame con el nombre de la PROVINCIA_NOMBRE y columnas para cada año con el código que le corresponde a esa PROVINCIA_NOMBRE en ese año
    
    Examples
    --------
    crear_df_provincias(df_provincias)
         
    '''
    # Crear un DataFrame vacío
    df_provincias_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_provincias.iterrows():
        # Revisar si la PROVINCIA_NOMBRE ya está en el dataframe
        if row["PROVINCIA_NOMBRE"] not in df_provincias_std.index:
            # Si la PROVINCIA_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_provincias_std.loc[row["PROVINCIA_NOMBRE"], row["ANIO"]] = row["PROVINCIA_CODIGO"]
        else:
            # Si la PROVINCIA_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_provincias_std.loc[row["PROVINCIA_NOMBRE"], row["ANIO"]] = row["PROVINCIA_CODIGO"]
    
    # Colocar las columnas de los años en orden
    df_provincias_std = df_provincias_std.reindex(sorted(df_provincias_std.columns), axis=1)
    # Colocar las filas en orden
    df_provincias_std = df_provincias_std.sort_index()
    return df_provincias_std



def recuperar_cantones(input_folder):
    '''
    Recupera todas los diccionarios de cantones de las elecciones y coloca los en un dataframe
    Se cambian las columnas para que no tengan caracteres especiales
    
    Paramaters
    ----------
        - input_folder: str 
            path al directorio que contiene los archivos .csv
    
    Returns
    -------
        - df_cantones: DataFrame
            DataFrame con los códigos de cantones de las elecciones
    
    Examples
    --------
    recuperar_cantones("data_csv")
         
    '''
    # Crear un DataFrame vacío
    df_cantones = pd.DataFrame()
    #De la carpeta, buscar el archivo que empieza con "cantones"
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith("cantones"):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #Los nombres de Cantones están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in ["CANTON_NOMBRE"] else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in ["CANTON_NOMBRE"] else x)
                    
                    #añadir el año de la elección al DataFrame
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_cantones = pd.concat([df_cantones, df])
    return df_cantones

def crear_df_cantones(df_cantones):
    '''
    Crea un data frame con el nombre de la CANTON_NOMBRE y columnas para cada año con el código que le corresponde a esa CANTON_NOMBRE en ese año.
    Si no hay código para esa CANTON_NOMBRE en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_cantones: DataFrame
            DataFrame con los códigos de cantones de las elecciones
    
    Returns
    -------
        - df_cantones_std: DataFrame
            DataFrame con el nombre de la CANTON_NOMBRE y columnas para cada año con el código que le corresponde a esa CANTON_NOMBRE en ese año
    
    Examples
    --------
    crear_df_cantones(df_cantones)
         
    '''
    # Crear un DataFrame vacío
    df_cantones_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_cantones.iterrows():
        # Revisar si la CANTON_NOMBRE ya está en el dataframe
        if row["CANTON_NOMBRE"] not in df_cantones_std.index:
            # Si la CANTON_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_cantones_std.loc[row["CANTON_NOMBRE"], row["ANIO"]] = row["CANTON_CODIGO"]
        else:
            # Si la CANTON_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_cantones_std.loc[row["CANTON_NOMBRE"], row["ANIO"]] = row["CANTON_CODIGO"]
    
    # Colocar las columnas de los años en orden
    df_cantones_std = df_cantones_std.reindex(sorted(df_cantones_std.columns), axis=1)
    # Colocar las filas en orden
    df_cantones_std = df_cantones_std.sort_index()
    return df_cantones_std

# Por lo pronto solo se estudia el codigo de la parroquia, no el canton ni la provincia
def recuperar_parroquias(input_folder):
    '''
    Recupera todas los diccionarios de parroquias de las elecciones y coloca los en un dataframe
    Se cambian las columnas para que no tengan caracteres especiales
    
    Paramaters
    ----------
        - input_folder: str 
            path al directorio que contiene los archivos .csv
    
    Returns
    -------
        - df_parroquias: DataFrame
            DataFrame con los códigos de parroquias de las elecciones
    
    Examples
    --------
    recuperar_parroquias("data_csv")
         
    '''
    # Crear un DataFrame vacío
    df_parroquias = pd.DataFrame()
    #De la carpeta, buscar el archivo que empieza con "parroquias"
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith("parroquias"):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #Los nombres de Parroquias están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in ["PARROQUIA_NOMBRE"] else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in ["PARROQUIA_NOMBRE"] else x)
                    
                    #añadir el año de la elección al DataFrame
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_parroquias = pd.concat([df_parroquias, df])
    return df_parroquias

def crear_df_parroquias(df_parroquias):
    '''
    Crea un data frame con el nombre de la PARROQUIA_NOMBRE y columnas para cada año con el código que le corresponde a esa PARROQUIA_NOMBRE en ese año.
    Si no hay código para esa PARROQUIA_NOMBRE en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_parroquias: DataFrame
            DataFrame con los códigos de parroquias de las elecciones
    
    Returns
    -------
        - df_parroquias_std: DataFrame
            DataFrame con el nombre de la PARROQUIA_NOMBRE y columnas para cada año con el código que le corresponde a esa PARROQUIA_NOMBRE en ese año
    
    Examples
    --------
    crear_df_parroquias(df_parroquias)
         
    '''
    # Crear un DataFrame vacío
    df_parroquias_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_parroquias.iterrows():
        # Revisar si la PARROQUIA_NOMBRE ya está en el dataframe
        if row["PARROQUIA_NOMBRE"] not in df_parroquias_std.index:
            # Si la PARROQUIA_NOMBRE no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_parroquias_std.loc[row["PARROQUIA_NOMBRE"], row["ANIO"]] = row["PARROQUIA_CODIGO"]
        else:
            # Si la PARROQUIA_NOMBRE ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_parroquias_std.loc[row["PARROQUIA_NOMBRE"], row["ANIO"]] = row["PARROQUIA_CODIGO"]
    
    # Colocar las columnas de los años en orden
    df_parroquias_std = df_parroquias_std.reindex(sorted(df_parroquias_std.columns), axis=1)
    # Colocar las filas en orden
    df_parroquias_std = df_parroquias_std.sort_index()
    return df_parroquias_std




# df_dignidades = recuperar_dignidades(input_folder)
# print(df_dignidades)
# df_dignidades_std = crear_df_dignidades(df_dignidades)
# print(df_dignidades_std)


# df_provincias = recuperar_provincias(input_folder)
# print(df_provincias)
# df_provincias_total=crear_df_provincias(df_provincias)
# print(df_provincias_total)
# df_provincias_total.to_csv("data_csv/Codigos_estandar/provincias_total.csv", index=True, header=True)


# df_cantones = recuperar_cantones(input_folder)
# #print(df_cantones)
# df_cantones_total=crear_df_cantones(df_cantones)
# print(df_cantones_total)
# df_cantones_total.to_csv("data_csv/Codigos_estandar/cantones_total.csv", index=True, header=True)

# df_parroquias=recuperar_parroquias(input_folder)
# #print(df_parroquias)
# df_parroquias_total=crear_df_parroquias(df_parroquias)
# print(df_parroquias_total)
# df_parroquias_total.to_csv("data_csv/Codigos_estandar/parroquias_total.csv", index=True, header=True)


#TODO: revisar las provincias a las que pertenecen los cantones por año
#TODO: revisar si hay parroquias que no pertenecen a un cantón
#TODO: revisar si hay parroquias que no pertenecen a una provincia

def recuperar_info(input_folder,dictionary_to_use, columns_to_preserve):
    '''
    Recupera todas los diccionarios de códigos de las elecciones y coloca los en un dataframe
    Se cambian los nombres de las columnas para que no tengan caracteres especiales
    Paramaters
    ----------
        - input_folder: str 
            path al directorio que contiene los archivos .csv
        - dictionary_to_use: str
            nombre del archivo que se quiere recuperar
        - columns_to_preserve: list
            lista con los nombres de las columnas que se quieren mantener
       
            
    
    Returns
    -------
        - df_info: DataFrame
            DataFrame con los códigos de la columna que se quiere recuperar el código
    
    Examples
    --------
    recuperar_info("data_csv", "dignidades", ["DIGNIDAD_NOMBRE", "DIGNIDAD_AMBITO"], "DIGNIDAD_CODIGO")
         
    '''
    # Crear un DataFrame vacío
    df_info = pd.DataFrame()
    # Listar todos los archivos en el directorio de entrada y sus subdirectorios
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".csv"):
                if file.startswith(dictionary_to_use):
                    # Construir el path del archivo
                    file_path = os.path.join(root, file)
                    # Leer el archivo en un DataFrame
                    df = pd.read_csv(file_path)
                    #camabiar los nombres de las columnas para que no tengan caracteres especiales
                    df.columns = [unidecode.unidecode(col) for col in df.columns]
                    #Los nombres y ambitos de las dignidades están en mayúsculas y tienen tildes y ñ.
                    #Vamos a mantenerlas en mayúsculas y vamos a quitarles los tildes y la ñ
                    df = df.apply(lambda x: x.str.upper() if x.name in columns_to_preserve else x)
                    df = df.apply(lambda x: x.apply(unidecode.unidecode) if x.name in columns_to_preserve else x)
                    #añadir el año de la elección al DataFrame
                    print(file)
                    año = re.findall(r'\d+', file)
                    df["ANIO"] = año[0]
                    # Agregar el DataFrame al DataFrame vacío
                    df_info = pd.concat([df_info, df])
    return df_info

def crear_df_info(df_info, column_to_study, column_to_use):
    '''
    Crea un data frame con el nombre de la columna que se quiere recuperar el código y ámbito geográfico.
    Y se van a crear columnas para cada año con el código que le corresponde a esa columna en ese año.
    Si no hay código para esa columna en ese año, se va a colocar un NaN
    
    Paramaters
    ----------
        - df_info: DataFrame
            DataFrame con los códigos de la columna que se quiere recuperar el código
        - column_to_study: str
            nombre de la columna que se está estudiando
        - column_to_use: str
            nombre de la columna que se quiere recuperar el código
    
    Returns
    -------
        - df_info_std: DataFrame
            DataFrame con el nombre de la columna que se quiere recuperar el código y ámbito geográfico y columnas para cada año con el código que le corresponde a esa columna en ese año
    
    Examples
    --------
    crear_df_info(df_info, ["DIGNIDAD_NOMBRE", "DIGNIDAD_AMBITO"], "DIGNIDAD_CODIGO")
         
    '''
    # Crear un DataFrame vacío
    df_info_std = pd.DataFrame()
    # Iterar sobre las filas del DataFrame
    for index, row in df_info.iterrows():
        # Revisar si la columna que se quiere recuperar el código ya está en el dataframe
        if row[column_to_study] not in df_info_std.index:
            # Si la columna que se quiere recuperar el código no está en el dataframe, agregarla y colocar su código en la columna correspondiente al año de la elección
            df_info_std.loc[row[column_to_study], row["ANIO"]] = row[column_to_use]
        else:
            # Si la columna que se quiere recuperar el código ya está en el dataframe, colocar su código en la columna correspondiente al año de la elección
            df_info_std.loc[row[column_to_study], row["ANIO"]] = row[column_to_use]
    
    # Colocar las columnas de los años en orden
    df_info_std = df_info_std.reindex(sorted(df_info_std.columns), axis=1)
    # Colocar las filas en orden
    df_info_std = df_info_std.sort_index()
    return df_info_std

df_cantones_provincia_codigo=recuperar_info(input_folder, "cantones", ["CANTON_NOMBRE", "PROVINCIA_NOMBRE"])
print(df_cantones_provincia_codigo)
df_cantones_provincia_codigo_std=crear_df_info(df_cantones_provincia_codigo, "CANTON_NOMBRE", "PROVINCIA_CODIGO")
print(df_cantones_provincia_codigo_std)
df_cantones_provincia_codigo_std.to_csv("data_csv/Codigos_estandar/all_cantones_provincia_codigo.csv", index=True, header=True)
