from requests.sessions import session
from prom import buscarPartidos
import tweepy
import schedule
import time
import config
import data as sp
import re
#Diccionario con equipos recolectados
todos = sp.total_equipos

#Autenticacion con la api de twitter (problemas con el acceso,limitan la cuenta)
auth = tweepy.OAuthHandler(consumer_key= config.API_KEY,consumer_secret=config.APY_KEY_SECRET)
auth.set_access_token(config.ACCESS_TOKEN,config.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True)


#Verificar si el nombre en el cuerpo del tweet coincide con un equipo valido, sino retorna 0
def checkEquipo(nombre):
    for key, value in todos.items():
        if nombre == key:
            return value
        else:
            return 0

#Lee el ultimo id de las menciones en twitter como punto de partida para responder los siguientes
def leerUltimoId():
    file = open('idtweets.txt','r')
    id = int(file.read().strip())
    file.close()
    return id

#Almacena el ultimo id del tweet ya respondido 
def guardarUltimoId(id):
    file = open('idtweets.txt', 'w')
    file.write(str(id))
    file.close()

#Chequea menciones en el orden que fueron twiteadas
#Lee el cuerpo del twit y llama a chechEquipo para verificar
def mentionCheck():
    patron = "@CuandoJuegaBot"
    mencion = api.mentions_timeline(since_id = leerUltimoId())
    for tweet in reversed(mencion):
        nom = re.sub(patron,'',tweet.text).lstrip()
        id = checkEquipo(nom)
        if(id > 0):
            data = buscarPartidos(id)
            tweetear(data,tweet)
        else:
            tweetear("Nombre incorrecto",tweet)

#Responde el tweet donde fue mencionada la cuenta con la informacion del proximo partido
#verificando si hay proximas fechas o no
def tweetear(df,twt):
    id = twt.id
    if df.empty:
        api.update_status(status= "No hay proximas fechas",in_reply_to_status_id= id)
    else:
        h = df.head(1).to_string(columns=['Dia','vsEquipo'],index = False,header = False)
        dia = re.findall(r'[0-9]+/+[0-9]+',h)
        eq = str(re.findall('[A-Z].+',h))

        cadena = '@'+twt.user.screen_name+' el dia: '+str(dia)+' vs: '+str(eq) #Mejorar el texto cadena que imprime
        api.update_status(status=cadena,in_reply_to_status_id= id)
        print('Se Twitteo')

    guardarUltimoId(id)


    

def main():
    schedule.every(10).seconds.do(mentionCheck)
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(2)
        except tweepy.TweepyException as e:
            raise e


if __name__ == "__main__":
	main()
    






