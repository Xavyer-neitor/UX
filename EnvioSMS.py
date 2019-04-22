import requests
import pymongo
from pprint import pprint
import time


def Mongoconexion():
	MONGODB_HOST = '13.52.11.40'
	MONGODB_PORT = '27017'
	MONGODB_TIMEOUT = 600000
	MONGODB_DATABASE = 'XLamudi'
	MONGODB_USER = 'Scraper%2Fops'
	MONGODB_PASS = 'R3vim3x5o5%2F%2F'

	URI_CONNECTION = "mongodb://" +MONGODB_USER+":"+MONGODB_PASS+"@"+ MONGODB_HOST + ":" + MONGODB_PORT +  "/admin"
 
	try:
		client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
		client.server_info()
		#print ('OK -- Connected to MongoDB at server %s' % (MONGODB_HOST))
		client.close()
	except pymongo.errors.ServerSelectionTimeoutError as error:
		#print ('Error with MongoDB connection: %s' % error)
		pass
	except pymongo.errors.ConnectionFailure as error:
		#print ('Could not connect to MongoDB: %s' % error)
		pass

	return client, MONGODB_DATABASE


cliente, base_datos = Mongoconexion()

def enviar_msm(a,b):
	
	collection = cliente[base_datos]['MSM']
	contactos = [x for x in collection.find({'Ranking':{'$gte':45},'Email':None})]
	#contactos = [x for x in collection.find( { '$and': [ { 'Nombre': 'Xavy R.' }, { 'Numero': { '$exists': True } } ] })]
	#pprint(contactos)
	contactos = contactos[a:b]

	nombres_cdt = [{'nm': x['Nombre']} for x in contactos]

	numeros_cdt = [{'phone': y['Numero']} for y in contactos]

	campaña_cdt = [{'camp_id':'02'} for x in range(len(nombres_cdt))]

	mensajes_cdt =  [{'message': z['Titulo'].replace('Bienvenido','Hola').replace('¿QUIERES VENDER MAS RAPIDO TU CASA? Cámbiate a un sitio web de mayor tráfico! http://bit.ly/letsnews0','¡ENTERATE! Esto es lo que tu web inmobiliaria gasta en publicidad! http://bit.ly/letshome1sm')} for z in contactos]

	LISTA_cdt = list(zip(nombres_cdt,campaña_cdt,numeros_cdt,mensajes_cdt))
	LISTA2_cdt = [list(j) for j in LISTA_cdt]

	newdict=[]

	for i in LISTA2_cdt:
		h={}
		for j in i:
			for k in j:
				h[k]=j[k]
		newdict.append(h)

	print('Enviando')
	print(len(newdict))
	url1 = 'http://commserver.letshomesupport.link:8181/sS_RVMX_f63d4E243'#otra buena
	url2 = 'http://35.211.230.71:8181/sS_RVMX_f63d4E243'#produccion
	url='http://192.168.2.215:8181/sS_RVMX_f63d4E243'#local


	files= {'messages':newdict}
	print('[X]-----------------------------')
	print(str({'messages':newdict}))	
	print('[X]-----------------------------')
	r = requests.post(url2,json=files)
	print(r.text)

for i in range(0,12):
	enviar_msm(i*1000,(i+1)*1000)
	time.sleep(600)
	






# borrado
# /* 1 */
# {
#     "_id" : ObjectId("5ca5767727308847e7c67024"),
#     "Nombre" : "Punto Fijo Bienes Raices",
#     "Email" : "elvira_alvarez@puntofijo.mx",
#     "Ranking" : 0,
#     "Titulo" : "¡Entérate! ¡Esto es lo que tu web inmobiliaria gasta en publicidad! ",
#     "url" : "http://bit.ly/letshome1em"
# }
	


