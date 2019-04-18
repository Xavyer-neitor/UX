import pymongo
import os
import json
import datetime
from bson.objectid import ObjectId
from bson import json_util


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

cliente,base_datos = Mongoconexion()

collection = cliente[base_datos]['prueba_cookies']
os.system('rm history_pages.json')

def datos_cookies():# funcion que devuelve un accion
	
	ip=[x for x in collection.find({},{'_id':0})]

	print(len(ip))

	print(ip[0])

	def fecha_to_dict(fecha):
		b =[a["fecha"].year,a["fecha"].month,a["fecha"].day,a["fecha"].hour]
		c= ["Año","Mes","Dia","hora"]
		new={}
		for ini in range(len(b)):
		   new[c[ini]]=b[ini]
			

	with open('history_pages.json','w') as f:
		f.write(str(ip).replace("'",'"'))

	with open('history_pages.json','r') as f:
		data = json.loads(f.read(),object_hook = json_util.object_hook)

	print(data)
if __name__ == '__main__':
	datos_cookies()



