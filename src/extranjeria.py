from typing import NamedTuple
import re
import csv
from collections import defaultdict
RegistroExtranjeria = NamedTuple(
    "RegistroExtranjeria", 
            [("distrito",str),
             ("seccion", str),
             ("barrio", str),
             ("pais",str),
             ("hombres", int),
             ("mujeres", int)
            ]
)
def lee_datos_extranjeria(ruta):
    registros=[]
    with open(ruta,encoding="utf-8") as f:
        lector=csv.reader(f)
        next(lector)
        for distrito,seccion,barrio,pais,hombres,mujeres in lector:
            distrito=str(distrito)
            seccion=str(seccion)
            hombres=int(hombres)
            mujeres=int(mujeres)
            tupla=RegistroExtranjeria(distrito,seccion,barrio,pais,hombres,mujeres)
            registros.append(tupla)
    return registros

def numero_nacionalidades_distintas(registros:list[RegistroExtranjeria]): 
    lista_paises_distintos=[]
    for a in registros:
        if a.pais  not  in lista_paises_distintos:
            lista_paises_distintos.append(a.pais)
    return len(lista_paises_distintos)

def secciones_distritos_con_extranjeros_nacionalidades(registros:list[RegistroExtranjeria], paises:set[str]):
    l=[]
    lista_barrios_con_paises=[]
    diccionario={}
    for a in registros:
        if a.pais in paises:
            if a.barrio not in diccionario:
             diccionario[a.barrio] = []  
        diccionario[a.barrio].append(a.pais)
    for a in diccionario:
        if set(diccionario[a]) == paises:
            l.append(a)
    for barrio in registros:
        if barrio.barrio in l:
            tupla=(barrio.distrito,barrio.seccion)
            lista_barrios_con_paises.append(tupla)
    return sorted(lista_barrios_con_paises,key=lambda x:x[0])

def total_extranjeros_por_pais(registros:list[RegistroExtranjeria]):
    diccionario=defaultdict(int)
    for dato in registros:
        diccionario[dato.pais]+=(dato.hombres+dato.mujeres)
    return diccionario


def top_n_extranjeria(registros, n=3):
    extranjeros_por_pais=total_extranjeros_por_pais(registros)
    return sorted(extranjeros_por_pais.items(),key=lambda x:x[0],reverse=True)[:n]


#print(top_n_extranjeria(registros))


def barrio_mas_multicultural(registros:list[RegistroExtranjeria])->str: 
    pais_por_barrio=obtener_paises_por_barrio(registros)
    total_ordenado=max(pais_por_barrio.items(),key=lambda x:len(pais_por_barrio.get(x)))
    return total_ordenado
  
    

def obtener_paises_por_barrio(registros:list[RegistroExtranjeria])->dict[str,set[str]]:
    res=defaultdict(set)
    for r in registros:
        res[r.barrio].add(r.pais)
    return res

def barrio_con_mas_extranjeros(registros:list[RegistroExtranjeria], tipo:str|None =None)->dict[str,int]:
    diccionario=defaultdict(int)
    for r in registros:
        if tipo==None:
            diccionario[r.barrio]+=r.mujeres+r.hombres
        elif tipo.lower()=="mujeres":
            diccionario[r.barrio]+=r.mujeres
        else:
            diccionario[r.barrio]+=r.hombres
    return max(diccionario,key=diccionario.get)


def pais_mas_representado_por_distrito(registros:list[RegistroExtranjeria])->dict[str:str]: 
    #las claves son los distritos y los valores los países
    # de los que hay más extranjeros residentes en cada dist
    #dicc clave distrito y como valor tuplas con el pais y su gente
    diccionario={}
    for a in registros:
        if a.distrito not in diccionario:
           diccionario[a.distrito]=[]
        diccionario[a.distrito].append((a.pais,a.hombres+a.mujeres))

    distrito_pais_con_mas_gente= {}
    for distrito, lista_paises in diccionario.items():
        pais_mas_gente = max(lista_paises, key=lambda x: x[1])[0] 
        distrito_pais_con_mas_gente[distrito] = pais_mas_gente
    return distrito_pais_con_mas_gente
      