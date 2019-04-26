import requests
import pymongo
from pprint import pprint
import time

# instrucciones de uso de envio de email con infografia,
#	1.-Mandar infografia a serafin, via Correo electronico, pedir que se suba al servidor(El genera el HTML del eaml)
#	2.-si son mas de una infografia, Mandarlos como listas , no importa el orden
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


def enviar_email(a,b):

	print('Enviando')
	#########################
	MENSAJE = '#ENTERATE: ESTAS WEBS INMOBILIARIAS SON TAN MALAS QUE NI LOS AVENGERS LAS SALVARIAN'
	LINKCORTO = 'http://bit.ly/letshome2em'######Cambiar para cada campaña ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
	CAMPAÑA = '03'######Cambiar para cada campaña ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
	INFOGRAFIAS =['INFOGRAFIA6-TOP5-REBOTE-PORC.jpg']#nombres de infografias 
	PRUEBA = False #Cambiar para enviar de verdad
	###########################
	##Base de Promotores
	collection = cliente[base_datos]['promotores_links']

	if PRUEBA:
		contactos = [x for x in collection.find({'email':{'$ne':None},"Origin":{'$exists':True}})]	
	else:
		contactos = [x for x in collection.find({'email':{'$ne':None},"Origin":{'$exists':False}})]
	
	print(len(contactos))
	contactos = contactos[a:b]

	nombres_cdt = [{'user': x['name']} for x in contactos]# En el email si se sigue usando el nombre del registro del promotor
	
	emails_cdt = [{'eml': y['email']} for y in contactos]

	campaña_cdt = [{'camp_id':CAMPAÑA} for x in range(len(nombres_cdt))]

	ID_cdt = [{'X-Model_ID':0} for x in range(len(nombres_cdt))]#preguntas a Serafin Sobre este campo

	img_cdt = [{'img':INFOGRAFIAS} for x in range(len(nombres_cdt))]

	mensajes_cdt =  [{'subtitulo': MENSAJE} for z in range(len(nombres_cdt))]#Subtitulo "h2" del html del correo

	subject_cdt =  [{'subject': ' Conoce más sobre el mercado inmobiliario'.format(nombres_cdt[z]['user'])} for z in range(len(nombres_cdt))]# Asunto por si se requiere personalizar, utilizar el {}format

	url_cdt =  [{'link1': LINKCORTO} for x in range(len(nombres_cdt))]


	LISTA_cdt = list(zip(nombres_cdt,campaña_cdt,img_cdt,ID_cdt,emails_cdt,mensajes_cdt,url_cdt,subject_cdt))
	LISTA2_cdt = [list(j) for j in LISTA_cdt]

	newdict=[]

	for i in LISTA2_cdt:
		h={}
		for j in i:
			for k in j:
				h[k]=j[k]
		newdict.append(h)

	print(len(newdict))
	pprint(newdict)

	url1 = 'http://commserver.letshomesupport.link:8181/sS_RVMX_f63d4E243'#otra buena
	url2 = 'http://35.211.230.71:8181/sendEmail_3890j4bffodj'#produccion
	url='http://192.168.2.215:8181/sendEmail_3890j4bffodj'#local


	files= {
			'messages':newdict,
			'plantilla':'prmTi_18_04_2019'#📐 Nombre de platilla de hmtl, Preguntas a serafin el nombre de la nueva por si se cambia la platilla 
			}
	print('[X]-----------------------------')
	pprint(str({'messages':newdict,'plantilla':'prmTi_18_04_2019'}))	
	print('[X]-----------------------------')
	r = requests.post(url2,json=files)
	print(r.text)
	
for i in range(0,37):
	enviar_email(i*100,(i+1)*100-1)
	time.sleep(1800)# Se envian 99 cada 30 min :(
		
