from bs4 import BeautifulSoup
import requests
import pandas as pd

#Busca los equipos y almacena el Nombre junto con su codigo propio de la pagina
def codigosEquipos(url):
    res = requests.get(url)
    sp = BeautifulSoup(res.content,'html.parser')
    j = 0 

    eq = sp.find(id='clubesnac').find_all_next('a')
    equipos = list()
    for i in eq:    
        equipos.append(i.get_text().replace('\n',''))

    cod = sp.find(id='clubesnac').find_all_next('a')
    dic = {}

  
    for i in equipos:
        indice = int(cod[j].get('href').replace('club=',''))
        dic[i] = indice
        j+=1
    return dic

#Busca el partido proximo dependiendo el id que se le pase y
def buscarPartidos(id):
    df = pd.read_html("https://www.promiedos.com.ar/club="+str(id), header=0, thousands="", decimal="," )[0]
    filtro = df['Ficha'] != 'add_box'
    nuevo_df = df[filtro]
    return nuevo_df.head(1)


    



