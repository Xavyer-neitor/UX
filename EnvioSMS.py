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


def enviar_msm(a,b,ranking):
	MENSAJE = '¡AY, COBRÓN! ESTAS WEBS INMOBILIARIAS TE COBRAN MUCHO POR PUBLICAR TU CASA.'.upper()# mensaje que se enviara en la campaña
	CAMPAÑA = '08'#Identificador o Nombre para saber en que campaña vamos la 1 o 2 o 3 ....⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
	LINKCORTO = 'http://bit.ly/letshome8sm'# Link corto correspondiente a la campaña⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
	PRUEBA = False
	#coleccion de los promotores Esquema:
		# {
		# 	"links":"valor lista, link de la propiedad asociada al promotor",
		# 	"name":"nombre del promotor",
		# 	"email":"correo del promotor, None en el caso de no tener",
		# 	"domain":"Lista, Los dominios donde estan las propiedades del promotor",
		# 	"ranking":"Calificaion basada en publicion",
		# 	"cruvs":"????",
		# 	"phone_clean":"Lista, Telefonos",
		# 	"phone":"Lista,Numero sin limpiar desde scraper",
		# 	"Origin":"Los que tengan 'LETSHOME', son a quienes se les envia la prueba :D!"
		# }
	collection = cliente[base_datos]['promotores_links'] 

	if PRUEBA:
		#Nosotros B)
		contactos = [x for x in collection.find({
													'Origin':'LETSHOME',
													'phone_clean':{
																	'$exists':True
																   }
												}
												)
					]
	elif not PRUEBA:
		#Contactos de Verdad :D!
		contactos = [y for y in collection.find({"$and":[{"scoring":{
																	'$gte':ranking
														  			}
														 },
														 {"$or":[
														 		{"contacted.status":True},
														 		{"contacted":{"$exists":False}}
														 		]
														 },
														 {"phone_clean":{
																			'$exists':True,
																			'$nin':[re.compile('/^044/')]
																		}
														 }
														 
														 ]
												},
												{
													#'_id':0,
													'cruvs':0,
													'links':0
												}
												)]
	

	contactos = contactos[a:b]#Envio por bloque de 1000
	nombres_cdt = [{'nm': x["name"]} for x in contactos]#Nombres para personalizar el mensaje
	numeros_cdt = [{'phone': y["phone_clean"][0]} for y in contactos]
	campaña_cdt = [{'camp_id':CAMPAÑA} for x in range(len(nombres_cdt))]
	mensajes_cdt = [{'message': MENSAJE+' '+LINKCORTO } for z in contactos]# Aqui!!! se tiene qye agregar el nombre para que sea personalizado
	promotor_id = [{"idP":str(w["_id"])} for w in contactos]
	LISTA_cdt = list(zip(nombres_cdt,campaña_cdt,numeros_cdt,mensajes_cdt,promotor_id))
	LISTA2_cdt = [list(j) for j in LISTA_cdt]

	newdict=[]#formato para envio a servidor de Comunicaciones de Serafau

	for i in LISTA2_cdt:
		h={}
		for j in i:
			for k in j:
				h[k]=j[k]
		newdict.append(h)

	print('Enviando')#print feo 
	pprint(newdict)

	#Servidores de prueba y produccion para Test :D!
	url1 = 'http://commserver.letshomesupport.link:8181/sS_RVMX_f63d4E243'#otra buena
	url2 = 'http://35.211.230.71:8181/sS_RVMX_f63d4E243'#produccion
	url='http://192.168.2.215:8181/sS_RVMX_f63d4E243'#local

	#Envio de la peticion para empezar el envio de sms
	files= {'messages':newdict}
	print('[X]-----------------------------')
	print(str({'messages':newdict}))	
	print('[X]-----------------------------')
	r = requests.post(url2,json=files)
	print(r.text)

for i in range(0,14):
	enviar_msm(i*1000,(i+1)*1000,ranking=40.3)
	time.sleep(300)# Cada 5 min

	


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
	

