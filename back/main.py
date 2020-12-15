#Librerias propias
import service, data


# Librerias requeridas para correr aplicaciones basadas en Flask
from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)


# Web service que se invoca al momento de ejecutar el comando
# curl http://localhost:5000
@app.route('/',methods = ['GET'])
def index():
	return "welcome"

#http://localhost:5000/api/getTweets/
@app.route('/api/getTweets/', methods = ['GET'])
def getTweets():
	return service.getTweets()

#http://localhost:5000/api/streaming/<word>
@app.route('/api/streaming/<string:word>',methods = ['GET'])
def streaming(word):
	return service.streaming(word)

#http://localhost:5000/api/startDemo/<word>
@app.route('/api/startDemo/<string:word>',methods = ['GET'])
def demo(word):
	return service.startDemo(word)

#http://localhost:5000/api/getDataForPieChart/
@app.route('/api/getDataForPieChart/',methods = ['GET'])
def getDataForPieChart():
	return service.getDataForPieChart()

#http://localhost:5000/api/getDataForLineChart/
@app.route('/api/getDataForLineChart/', methods = ['GET'])
def getDataForLineChart():
	return service.getDataForLineChart()

#http://localhost:5000/api/getWordCloud/
@app.route('/api/getWordCloud/<string:word>', methods = ['GET'])
def getWordCloud(word):
	return service.getWordCloud()

#http://localhost:5000/api/getCounters/
@app.route('/api/getCounters/', methods = ['GET'])
def getCounters():
	return service.getCounters()

#http://localhost:5000/api/exportExcel/
@app.route('/api/exportExcel/<string:word>', methods = ['GET'])
def exportExcel(word):
	return service.exportExcel()

#http://localhost:5000/api/exportCSV/
@app.route('/api/exportCSV/<string:word>', methods = ['GET'])
def exportCSV(word):
	return service.exportCSV()

#capturadores de errores 404 y 405
@app.errorhandler(404)
def not_foud(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_foud(error):
	return make_response(jsonify({'error': 'Not Exist'}), 405)

if __name__ == '__main__':
        app.run(debug = False, host='0.0.0.0', port=5000)
