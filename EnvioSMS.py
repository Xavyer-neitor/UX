import requests
import pymongo
from pprint import pprint
import time
import re

def Mongoconexion():
	MONGODB_HOST = '18.222.106.24'
	MONGODB_PORT = '12012'
	MONGODB_TIMEOUT = 600000
	MONGODB_DATABASE = 'Promotores'
	MONGODB_USER = 'u_Main_admin'
	MONGODB_PASS = 'SDVeR3)8u9234&(234'
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
	MENSAJE = '#ENTERATE: ESTAS WEBS INMOBILIARIAS SON TAN MALAS QUE NI LOS AVENGERS LAS SALVARIAN'
	CAMPAÑA = '03'
	LINKCORTO = 'http://bit.ly/letshome2sm'
	PRUEBA = True
	collection = cliente[base_datos]['promotores_links'] 

	if PRUEBA:
		contactos = [x for x in collection.find({'Origin':'LETSHOME','phone_clean':{'$exists':True}})]
	elif not PRUEBA:
		contactos = [y for y in collection.find({"ranking":{'$gte':60},"phone_clean":{'$exists':True,'$nin':[re.compile('/^044/')]}},{'_id':0,'cruvs':0,'links':0})]
	

	contactos = contactos[a:b]
	nombres_cdt = [{'nm': x["name"]} for x in contactos]
	numeros_cdt = [{'phone': y["phone_clean"][0]} for y in contactos]
	campaña_cdt = [{'camp_id':CAMPAÑA} for x in range(len(nombres_cdt))]
	mensajes_cdt = [{'message': '¡HOLA! '+MENSAJE+' '+LINKCORTO } for z in contactos]
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
	pprint(newdict)
	url1 = 'http://commserver.letshomesupport.link:8181/sS_RVMX_f63d4E243'#otra buena
	url2 = 'http://35.211.230.71:8181/sS_RVMX_f63d4E243'#produccion
	url='http://192.168.2.215:8181/sS_RVMX_f63d4E243'#local


	# files= {'messages':newdict}
	# print('[X]-----------------------------')
	# print(str({'messages':newdict}))	
	# print('[X]-----------------------------')
	# r = requests.post(url2,json=files)
	# print(r.text)

for i in range(0,14):
	enviar_msm(i*1000,(i+1)*1000)
	time.sleep(300)

	


# # borrado
# /* 1 */
# {
#     "_id" : ObjectId("5ca5767727308847e7c67024"),
#     "Nombre" : "Punto Fijo Bienes Raices",
#     "Email" : "elvira_alvarez@puntofijo.mx",
#     "Ranking" : 0,
#     "Titulo" : "¡Entérate! ¡Esto es lo que tu web inmobiliaria gasta en publicidad! ",
#     "url" : "http://bit.ly/letshome1em"
# }
	

