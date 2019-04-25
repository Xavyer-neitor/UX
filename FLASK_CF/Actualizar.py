
from pymongo import MongoClient
import requests
from datetime import datetime

#La función shortlinks actualiza en la base los enlaces acortados creados
#para campaña sms y email
# link_corto es el enlace acortado
#link_largo es el enlace normal
#campaña puede ser 'sms' o 'email'
#clave es el identificador de la campaña actual, las primeras fueron '01'y '02'.
#enviados es el numero total de sms que se enviaran o emails dependiendo


#Titulo= '¡ENTERATE! Estas webs inmobiliarias son tan malas que ni los Avengers las salvarían'

def shortlinks(link_corto,link_largo,campaña,clave,total_enviados,Titulo):

	db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@13.52.11.40:27017/admin').XLamudi
	collection = db['bitly']
	datos = {'link_corto':link_corto,
			 'link_largo':link_largo,
			 'fecha_creacion':datetime.now(),
			 'campaña':campaña,
			 'camp_id':clave,
			 "enviados" : total_enviados,
			 "Titulo":Titulo
	}
	collection.insert(datos)
	print('[X]--correcto--[X]')


if __name__ == "__main__":
	shortlinks('http://bit.ly/letshome2em','https://www.letshome.mx/blog/Guacala-de-pollo-Estas-son-las-webs-inmobiliarias-que-menos-gustan-a-la-gente_5cbdf3905770491516a4d7b4?email','email','03',3555,'#ENTERATE: ESTAS WEBS INMOBILIARIAS SON TAN MALAS QUE NI LOS AVENGERS LAS SALVARIAN')
	#shortlinks('http://bit.ly/letsnews1','https://letshome.mx/blog/5caffa0fe43805f2c2063ea8','sms','03',11232)

