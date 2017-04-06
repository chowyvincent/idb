from app import app, db
from app.models import Agency, Launch, Location, Mission
from flask import render_template, jsonify, request
import json
import os
import subprocess
import urllib

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/agencies')
def agencies():
	return render_template("agencies.html")

@app.route('/launches')
def launches():
	return render_template("launches.html")

@app.route('/locations')
def locations():
	return render_template("locations.html")

@app.route('/missions')
def missions():
	return render_template("missions.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/about/testResults', methods=['GET'])
def getTestResults():
	#s = subprocess.check_output(['python3','./tests.py'])
	path = os.path.dirname(os.path.realpath(__file__))
	p = subprocess.check_output(['python3', os.path.join(path, '../tests.py')], stderr=subprocess.STDOUT)
	## But do not wait till netstat finish, start displaying output immediately ##
	print(p)
	l = [{"testResults" : p.decode('utf-8')}]#out.decode('utf-8')}]
	# i = 1
	# p.stdout.readline()
	# p.stdout.readline()
	# while True and i > 0:
	# 	out = p.stdout.read()
	# 	if out == '' and p.poll() != None:
	# 		break
	# 	if out != '':
	# 		print(out)
	# 	i-=1
	# print(out)

	return jsonify(l)


#API
@app.route('/api/<model>')
def api_model(model):
	print("---------------------------DEBUG----------------------------------")
	print(urllib.parse.unquote(str(request.query_string)))
	print("---------------------------DEBUG----------------------------------")
	NUM_PER_PAGE = 12
	l = []
	m = getModel(model)[0]

	req_str = urllib.parse.unquote(str(request.query_string)[2:-1])
	if len(req_str) == 0:
		query_list = m.query.all()
	elif len(req_str.split("&")) == 1 and "id" in req_str:
		query_list = m.query.filter_by(id=req_str.replace("id=", ""))
	else:
		split_req_str = req_str.split("&")
		str_dict = {'orderBy':None,'order':'asc','page':1,'limit':NUM_PER_PAGE}

		#Check which model (agency, launch, location, mission)
		#and change str_dict accordingly with default None values
		if model == 'agency':
			str_dict['agencyType'] = None
		elif model == 'launch':
			str_dict['status'] = None
		elif model == 'location':
			str_dict['countryCode'] = None
		elif model == 'mission':
			str_dict['missionType'] = None

		for pair in split_req_str:
			split_eq = pair.split("=")
			str_dict[split_eq[0]] = split_eq[1]

		criteria = str_dict['orderBy'] if str_dict['orderBy'] in m.attributes() else None
		page_num = int(str_dict['page'])
		page_num = page_num if page_num >= 1 else 1

		query_list = m.query

		if model == 'agency':
			query_list = query_list.filter_by(agencyType=str_dict['agencyType'])
		elif model == 'launch':
			query_list = query_list.filter_by(status=str_dict['status'])
		elif model == 'location':
			query_list = query_list.filter_by(countryCode=str_dict['countryCode'])
		elif model == 'mission':
			query_list = query_list.filter_by(missionType=str_dict['missionType'])

		if(str_dict['order'] == 'desc'):
			#query_list = m.query.order_by(desc(criteria)).paginate(page_num, str_dict['limit'], False).items
			query_list = query_list.order_by(desc(criteria)).paginate(page_num, str_dict['limit'], False).items
		else:
			#query_list = m.query.order_by(criteria).paginate(page_num, str_dict['limit'], False).items
			query_list = query_list.order_by(criteria).paginate(page_num, str_dict['limit'], False).items
		if query_list == []:
			return "<h1>Page "+str(str_dict['page'])+" does not contain any "+model+".</h1>"

	for obj in query_list:
		d = obj.dictionary()
		l.append(d)
	return jsonify(l)

@app.route('/<model>')
@app.route('/<model>/<int:page>')
def models(model, page=1):
	NUM_PER_PAGE = 12
	l = []
	info = getModel(model)
	m = info[0]
	if m == -1:
		return "<h1>Model not found</h1>"

	# print("---------------------------DEBUG----------------------------------")
	# # print(request.query_string)
	# print(urllib.parse.unquote(str(request.query_string)))
	# print("---------------------------DEBUG----------------------------------")

	#filtwerin still not working
	query_list = m.query.filter_by().paginate(page, NUM_PER_PAGE, False).items
	if query_list == []:
		return "<h1>Page "+str(page)+" does not contain any "+model+".</h1>"
	for obj in query_list:
		d = obj.dictionary()
		l.append(d)
	# return jsonify(l)
	return render_template(info[1]+".html",models=l)

# @app.route('/api/<model>/<criteria>/<int:page>/<filter>')
# def api_model_criteria_page_filter(model, criteria, page, filter):
# 	#url: /api/agency/name/1/filter?countryCode=USA
# 	#Use request.query_string to get the parameter to filter with
#     return request.query_string
####

# temperal route to dummy pages 
# Should be removed later!!!!!
@app.route('/agencies?id=1')
def agency_1():
	return render_template("temp/agency_1.html");

@app.route('/agencies?id=2')
def agency_2():
	return render_template("temp/agency_2.html");

@app.route('/agencies?id=3')
def agency_3():
	return render_template("temp/agency_3.html");

@app.route('/launches?id=1')
def launches_1():
	return render_template("temp/launches_1.html");

@app.route('/launches?id=2')
def launches_2():
	return render_template("temp/launches_2.html");

@app.route('/launches?id=3')
def launches_3():
	return render_template("temp/launches_3.html");

@app.route('/locations?id=1')
def location_1():
	return render_template("temp/location_1.html");

@app.route('/locations?id=2')
def location_2():
	return render_template("temp/location_2.html");

@app.route('/locations?id=3')
def location_3():
	return render_template("temp/location_3.html");

@app.route('/missions?id=1')
def mission_1():
	return render_template("temp/mission_1.html");

@app.route('/missions?id=2')
def mission_2():
	return render_template("temp/mission_2.html");

@app.route('/missions?id=3')
def mission_3():
	return render_template("temp/mission_3.html");


#UTILITY METHODS
def getModel(model):
	if model == 'agency':
		return (Agency, "agencies")
	elif model == 'launch':
		return (Launch, "launches")
	elif model == 'location':
		return (Location, "locations")
	elif model == 'mission':
		return (Mission, "missions")
	else:
		return -1


