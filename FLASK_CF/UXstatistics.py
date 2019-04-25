import time
from flask import Flask,render_template,request,jsonify,url_for,json
from pymongo import *
from bson.objectid import ObjectId
from pprint import pprint
import dateutil.parser as parser
import calendar
import json
from flask_cors import CORS
import pygal
from pygal.style import Style
import requests
import html
app = Flask(__name__)
 
@app.route("/")
def home():
	return render_template('frontUX.html')

@app.route("/analytics")
def analytics():
	return render_template('analytics.html')

@app.route("/heatmap")
def heatmap():
	return render_template('heatmap.html')

@app.route("/flujo")
def flujo():
	return render_template('flujo.html')

@app.route("/email")
def email():

	#trabajar desde una base de datos
	db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@13.52.11.40:27017/admin').XLamudi
	db2 = MongoClient('mongodb://commserver:pbn2OpfekjfZnp?2v49183D09.f93nv049u@35.227.93.9:27017/admin').commserver
	collection = db['bitly']
	enlaces=[x for x in collection.find({})]
	collection2 = db2['deliveredmsgs']
	collection3 = db2['deliveredmails']
	sms = [y for y in collection2.find({})]
	email = [z for z in collection3.find({})]
	tokenbitly = 'e51c52061b3675fd00e523dfa557bd5efd21558e' #token para api
	url='https://api-ssl.bitly.com/v3/user/popular_links?access_token={}'
	r = json.loads((requests.get(url.format(tokenbitly)).content).decode('utf-8'))
	historial = r['data']['popular_links']
	links_populares = []
	for i in historial:
		for k in enlaces:
			if i['link'] == k['link_corto']:
				links_populares.append({'enlace':i['link'],'clicks':i['clicks'],'enlace_real':k['link_largo'],'tipo':k['campaña'],"camp_id":k["camp_id"],"enviados":k["enviados"],"Titulo":k["Titulo"],"Fecha":str(k["fecha_creacion"].year)+'/'+str(k["fecha_creacion"].month)+'/'+str(k["fecha_creacion"].day)})
	total_campsms = [x for x  in collection2.distinct('camp_id')]
	total_campema = [x for x  in collection3.distinct('camp_id')]
	total_campanasms= []
	for i in links_populares:
		for j in [x for x  in collection2.distinct('camp_id')]:
			if j==i['camp_id'] and i['tipo']=='sms':
				total_campanasms.append({'enlace':i['enlace'],'camp_id':j,'entregados':collection2.find({"camp_id":j}).count()})
	for i in links_populares:
		for j in total_campanasms:
			if i['enlace'] == j['enlace']:
				 i['entregados'] = j['entregados']
	total_campanaema= []
	for i in links_populares:
		for j in [x for x  in collection3.distinct('camp_id')]:
			if j==i['camp_id'] and i['tipo']=='email':
				total_campanaema.append({'enlace':i['enlace'],'camp_id':j,'entregados':collection3.find({"camp_id":j}).count()})
	for i in links_populares:
		for j in total_campanaema:
			if i['enlace'] == j['enlace']:
				 i['entregados'] = j['entregados']
	#lp={}
	lp=[]
	for i in range(len(links_populares)):
		if links_populares[i]['tipo'] == 'email':
			#lp[i]=links_populares[i]
			lp.append(links_populares[i])

	return render_template('email.html', lp=json.dumps(lp))


@app.route("/sms")
def sms():

	#trabajar desde una base de datos
	db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@13.52.11.40:27017/admin').XLamudi
	db2 = MongoClient('mongodb://commserver:pbn2OpfekjfZnp?2v49183D09.f93nv049u@35.227.93.9:27017/admin').commserver
	collection = db['bitly']
	enlaces=[x for x in collection.find({})]
	collection2 = db2['deliveredmsgs']
	collection3 = db2['deliveredmails']
	sms = [y for y in collection2.find({})]
	email = [z for z in collection3.find({})]
	tokenbitly = 'e51c52061b3675fd00e523dfa557bd5efd21558e' #token para api
	url='https://api-ssl.bitly.com/v3/user/popular_links?access_token={}'
	r = json.loads((requests.get(url.format(tokenbitly)).content).decode('utf-8'))
	historial = r['data']['popular_links']
	links_populares = []
	for i in historial:
		for k in enlaces:
			if i['link'] == k['link_corto']:
				links_populares.append({'enlace':i['link'],'clicks':i['clicks'],'enlace_real':k['link_largo'],'tipo':k['campaña'],"camp_id":k["camp_id"],"enviados":k["enviados"],"Titulo":k["Titulo"],"Fecha":str(k["fecha_creacion"].year)+'/'+str(k["fecha_creacion"].month)+'/'+str(k["fecha_creacion"].day)})
	total_campsms = [x for x  in collection2.distinct('camp_id')]
	total_campema = [x for x  in collection3.distinct('camp_id')]
	total_campanasms= []
	for i in links_populares:
		for j in [x for x  in collection2.distinct('camp_id')]:
			if j==i['camp_id'] and i['tipo']=='sms':
				total_campanasms.append({'enlace':i['enlace'],'camp_id':j,'entregados':collection2.find({"camp_id":j}).count()})
	for i in links_populares:
		for j in total_campanasms:
			if i['enlace'] == j['enlace']:
				 i['entregados'] = j['entregados']
	total_campanaema= []
	for i in links_populares:
		for j in [x for x  in collection3.distinct('camp_id')]:
			if j==i['camp_id'] and i['tipo']=='email':
				total_campanaema.append({'enlace':i['enlace'],'camp_id':j,'entregados':collection3.find({"camp_id":j}).count()})
	for i in links_populares:
		for j in total_campanaema:
			if i['enlace'] == j['enlace']:
				 i['entregados'] = j['entregados']
	lp=[]
	for i in range(len(links_populares)):
		if links_populares[i]['tipo'] == 'sms':
			#lp[i]=links_populares[i]
			lp.append(links_populares[i])


	return render_template('sms.html', lp=json.dumps(lp))

@app.route("/bitly")
def bitly():

	#trabajar desde una base de datos
	db = MongoClient('mongodb://Scraper%2Fops:R3vim3x5o5%2F%2F@13.52.11.40:27017/admin').XLamudi
	db2 = MongoClient('mongodb://commserver:pbn2OpfekjfZnp?2v49183D09.f93nv049u@35.227.93.9:27017/admin').commserver
	collection = db['bitly']
	enlaces=[x for x in collection.find({})]
	collection2 = db2['deliveredmsgs']
	collection3 = db2['deliveredmails']
	sms = [y for y in collection2.find({})]
	email = [z for z in collection3.find({})]
	tokenbitly = 'e51c52061b3675fd00e523dfa557bd5efd21558e' #token para api
	url='https://api-ssl.bitly.com/v3/user/popular_links?access_token={}'
	r = json.loads((requests.get(url.format(tokenbitly)).content).decode('utf-8'))
	historial = r['data']['popular_links']
	links_populares = []
	for i in historial:
		for k in enlaces:
			if i['link'] == k['link_corto']:
				links_populares.append({'enlace':i['link'],'clicks':i['clicks'],'enlace_real':k['link_largo'],'tipo':k['campaña'],"camp_id":k["camp_id"],"enviados":k["enviados"],"Fecha":str(k["fecha_creacion"].year)+'/'+str(k["fecha_creacion"].month)+'/'+str(k["fecha_creacion"].day)})
	total_campsms = [x for x  in collection2.distinct('camp_id')]
	total_campema = [x for x  in collection3.distinct('camp_id')]
	total_campanasms= []
	for i in links_populares:
		for j in [x for x  in collection2.distinct('camp_id')]:
			if j==i['camp_id'] and i['tipo']=='sms':
				total_campanasms.append({'enlace':i['enlace'],'camp_id':j,'entregados':collection2.find({"camp_id":j}).count()})
	for i in links_populares:
		for j in total_campanasms:
			if i['enlace'] == j['enlace']:
				 i['entregados'] = j['entregados']
	total_campanaema= []
	for i in links_populares:
		for j in [x for x  in collection3.distinct('camp_id')]:
			if j==i['camp_id'] and i['tipo']=='email':
				total_campanaema.append({'enlace':i['enlace'],'camp_id':j,'entregados':collection3.find({"camp_id":j}).count()})
	for i in links_populares:
		for j in total_campanaema:
			if i['enlace'] == j['enlace']:
				 i['entregados'] = j['entregados']

	chart = pygal.Bar()
	custom_style = Style(
	colors=('#E80080', '#404040', '#9BC850','#E80080', '#404040'))

	chart = pygal.Bar(margin=40)
	chart = pygal.Bar(width=180)
	chart = pygal.Bar(height=280)
	chart.title = 'total interacciones por enlace campaña sms-email'
	

	for i in links_populares:
		chart.add(str([i["camp_id"]])+i['tipo']+' '+'enviados:'+str(i['enviados'])+' '+'entregados:'+str([i['entregados']])+str(int((i['entregados']*100)/i['enviados']))+'%'+' '+'interaccion:'+str(int((i['clicks']*100)/i['entregados']))+'%',[{'value':i['clicks'],'label':'clicks'}])
		
	chart.render_to_file('static/images/bar_chart.svg')
	img_url = 'static/images/bar_chart.svg?cache=' + str(time.time())

	return render_template('app.html',image_url = img_url)

if __name__ == "__main__":
	app.run()
