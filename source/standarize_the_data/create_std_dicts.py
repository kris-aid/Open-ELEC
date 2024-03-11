# Este script es para generar los diccionarios estandarizados de las dignidades, parroquias, cantones, provincias

# Path: source/standarize_the_data/create_std_dicts.py

import os
import pandas as pd
import numpy as np
import re
import sys
import unidecode
class Standard_Dictionaries:
    '''
    Clase para estandarizar los diccionarios de las elecciones
    
    Examples
    --------
    
    input_folder = "data_csv/seccionales/2023/diccionarios"
    std_dicts = Standard_Dictionaries(input_folder)
    std_dicts.change_to_std_dignidades()
    
    '''
    def __init__(self, input_folder):
        '''
        Inicializa la clase
        Parameters
        ----------
            - input_folder: str 
                path al directorio que contiene los archivos .csv
        '''
        self.input_folder = input_folder
        self.df_dignidades = self.recuperar_dignidades()
        # self.df_parroquias = self.recuperar_parroquias()
        # self.df_cantones = self.recuperar_cantones()
        self.df_provincias = self.recuperar_provincias()
        
    def recuperar_dignidades(self):
        '''
        Recupera todas los diccionarios de dignidades de las elecciones y coloca los en un dataframe
        Se cambian las columnas para que no tengan caracteres especiales
        
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
        #De la carpeta, buscar el archivo que empieza con "dignidades"
        for root, dirs, files in os.walk(self.input_folder):
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
                        print("gola")
                        print(df_dignidades)
        return df_dignidades
    
    def change_to_std_dignidades(self):
        '''
        Cambia los nombres y códigos de las dignidades a los nombres y códigos estandarizados
        
        Paramaters
        ----------
            - df_dignidades: DataFrame
                DataFrame con los códigos de dignidades de las elecciones
                
        
        Returns
        -------
            - df_dignidades: DataFrame
                DataFrame con los códigos de dignidades de las elecciones estandarizados    
    
        '''
        
        # Antes del 2007, el codigo 3 es para los concejos provinciales
        dict_dignidades_std_pre_2007 = { "DIGNIDAD_CODIGO":[1, 2, 3, 4, 5, 6, 7, 8],
                            "DIGNIDAD_NOMBRE":["PRESIDENCIA", "PREFECTURA", "CONCEJO PROVINCIAL", "ALCALDIA", "CONCEJO URBANO", "JUNTA PARROQUIAL", "ASAMBLEA PROVINCIAL", "PARLAMENTO ANDINO"],
                             "DIGNIDAD_AMBITO":["NACIONAL", "PROVINCIAL", "PROVINCIAL", "CANTONAL", "CANTONAL", "PARROQUIAL", "PROVINCIAL", "NACIONAL"]}
        
        
        #
        dict_dignidades_std_post_2007 = { "DIGNIDAD_CODIGO":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                           "DIGNIDAD_NOMBRE":["PRESIDENCIA", "PREFECTURA", "CONCEJO RURAL", "ALCALDIA", "CONCEJO URBANO", "JUNTA PARROQUIAL", "ASAMBLEA PROVINCIAL", "PARLAMENTO ANDINO", "ASAMBLEA NACIONAL", "ASAMBLEA CIRCUNSCRIPCION", "CPCCS M", "CPCCS H", "CPCCS NAC/EXT"],
                            "DIGNIDAD_AMBITO":["NACIONAL", "PROVINCIAL", "CANTONAL", "CANTONAL", "CANTONAL", "PARROQUIAL", "PROVINCIAL", "NACIONAL", "NACIONAL", "PROVINCIAL", "NACIONAL", "NACIONAL", "NACIONAL"]}
        
        #pd.DataFrame(dict_dignidades_std_post_2007).to_csv("data_csv/Codigos_estandar/dignidades/dignidades_std_post_2007.csv", index=False)
        #pd.DataFrame(dict_dignidades_std_pre_2007).to_csv("data_csv/Codigos_estandar/dignidades/dignidades_std_pre_2007.csv", index=False)
        
        # Hay un problema en ciertos años. Los códigos de las dignidades no son los mismos que los del diccionario o que los nombres de las dignidades no son los mismos que los del diccionario
        # Vamos a tener un diccionario de las equivalencias de los nombres de las dignidades
        # Por ejemplo si el nombre de la dignidad es PRESIDENTA/E Y VICEPRESIDENTA/E o PRESIDENTE Y VICEPRESIDENTE vamos a cambiarlo a PRESIDENCIA
        # Si el nombre de la dignidad es CONCEJALES RURALES vamos a cambiarlo a CONCEJO RURAL
        # Si el nombre de la dignidad es ALCALDES o ALCALDE MUNICIPAL o ALCALDES MUNICIPALES o ALCANCESA/ALCALDE vamos a cambiarlo a ALCALDIA
        # Si el nombre de la dignidad es CONCEJALES MUNICIPALES vamos a cambiarlo a CONCEJO MUNICIPAL
        
        dict_equivalencias= {
                            "PRESIDENCIA": ["PRESIDENTA/E Y VICEPRESIDENTA/E", "PRESIDENTE Y VICEPRESIDENTE"],
                            "PREFECTURA": ["PREFECTA / PREFECTO","PREFECTO PROVINCIAL", "PREFECTO Y VICEPREFECTO"],
                            "ALCALDIA": ["ALCALDES", "ALCALDE MUNICIPAL", "ALCALDES MUNICIPALES", "ALCALDESA / ALCALDE"],
                            "ASAMBLEA NACIONAL":["ASAMBLEISTAS NACIONALES"],
                            "ASAMBLEA PROVINCIAL": ["ASAMBLEISTAS PROVINCIALES", "ASAMBLEISTAS PROVINCIALES Y DEL EXTERIOR","DIPUTADOS PROVINCIALES"],
                            "ASAMBLEA CIRCUNSCRIPCION":["ASAMBLEISTAS POR CIRCUNSCRIPCION"],
                            "CONCEJO URBANO": ["CONCEJALES MUNICIPALES", "CONCEJALES URBANOS", "CONCEJAL MUNICIPAL"],
                            "CONCEJO RURAL": ["CONCEJALES RURALES"],
                            "CONCEJO PROVINCIAL": ["CONSEJEROS PROVINCIALES","CONSEJERO PROVINCIAL"],
                            "JUNTA PARROQUIAL": ["JUNTAS PARROQUIALES","MIEMBROS JUNTAS PARROQUIALES","VOCALES DE JUNTA PARROQUIAL",
                                                "VOCALES DE JUNTAS PARROQUIALES","VOCALES JUNTAS PARROQUIALES"],
                            "PARLAMENTO ANDINO": ["PARLAMENTARIOS ANDINOS"],
                            "CPCCS M": ["CPCCS (MUJERES)"],
                            "CPCCS H": ["CPCCS (HOMBRES)"],
                            "CPCCS NAC/EXT": ["CPCCS (NAC/EXT)"]}
        
        #Vamos a cambiar los nombres de las dignidades
        #Primero vamos a cambiar los nombres de las dignidades que no son los mismos que los del diccionario
        for key, value in dict_equivalencias.items():
            for v in value:
                self.df_dignidades.loc[self.df_dignidades["DIGNIDAD_NOMBRE"]==v, "DIGNIDAD_NOMBRE"] = key
    
        
                
        #Si el año es antes del 2007, vamos a usar el diccionario de las dignidades antes del 2007
        if self.df_dignidades["ANIO"].astype(int).max() < 2007:
            codigos_std=pd.DataFrame(dict_dignidades_std_pre_2007)
        # Si el año es después del 2007, vamos a usar el diccionario de las dignidades después del 2007    
        else:
            codigos_std=pd.DataFrame(dict_dignidades_std_post_2007)
        
        # Vamos a hacer un left join con el DataFrame de las dignidades estandarizadas
        self.df_dignidades = self.df_dignidades.merge(codigos_std, on="DIGNIDAD_NOMBRE", how="left")
        # Y nos quedamos con los códigos estandarizados
        self.df_dignidades["DIGNIDAD_CODIGO"] = self.df_dignidades["DIGNIDAD_CODIGO_y"]
        self.df_dignidades["DIGNIDAD_AMBITO"] = self.df_dignidades["DIGNIDAD_AMBITO_x"]
        self.df_dignidades["DIGNIDAD_CODIGO_OLD"] = self.df_dignidades["DIGNIDAD_CODIGO_x"]
        #self.df_dignidades["DIGNIDAD_NOMBREs_OLD"] = self.df_dignidades["DIGNIDAD_NOMBRE"]
        # Eliminamos las columnas que no necesitamos
        self.df_dignidades = self.df_dignidades.drop(columns=["DIGNIDAD_CODIGO_x", "DIGNIDAD_CODIGO_y","DIGNIDAD_AMBITO_x","DIGNIDAD_AMBITO_y", "ANIO"])

    def recuperar_provincias(self):
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
        for root, dirs, files in os.walk(self.input_folder):
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
        
       
        
    
    

#Test del metodo para el año 2013
input_folder = "data_csv/generales/2002/diccionarios"
std_dicts = Standard_Dictionaries(input_folder)
#print(std_dicts.df_dignidades)
std_dicts.change_to_std_dignidades()
print(std_dicts.df_dignidades)
#print(std_dicts.df_provincias)