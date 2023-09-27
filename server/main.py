from flask import Flask, redirect, url_for, request, abort, render_template
from flask_cors import CORS
from flask_selfdoc import Autodoc
from database import MongoDB
import pandas as pd

app = Flask(__name__)
CORS(app)
auto_doc = Autodoc(app)
dB = MongoDB()
dB.connect()

@app.route("/api/v1/create", methods=['POST'])
@auto_doc.doc()
def create():
	"""
	This can be used to create a new license
	"""
	try:
		response = dB.create(request.get_json())
		return {'message': 'Created a new license', 'id': response}, 200
	except Exception as e:
		return {'message': str(e)}, 400

@app.route("/api/v1/renew", methods=['PATCH'])
@auto_doc.doc()
def renew():
	"""
	This can be used to renew a license
	"""
	try:
		dB.renew(request.get_json())
		return {'message': 'Renewed the license'}, 200
	except Exception as e:
		return {'message': str(e)}, 400

@app.route("/api/v1/delete", methods=['DELETE'])
@auto_doc.doc()
def delete():
	"""
	This can be used to delete a license
	"""
	try:
		dB.delete(request.get_json())
		return {'message': 'Deleted the license'}, 200
	except Exception as e:
		return {'message': str(e)}, 400

@app.route("/api/v1/validate", methods=['GET'])
@auto_doc.doc()
def validate():
	"""
	This can be used to validate a license
	"""
	try:
		response = dB.validate(request.get_json())
		return {'message': 'Validated the license', 'license-details': response}, 200
	except Exception as e:
		return {'message': str(e)}, 404
	
@app.route("/api/v1/get-all", methods=['GET'])
def getAll():
	"""
	This can be used to get all the licenses from database
	"""
	try:
		response = dB.getAll()
		return {'license-database': response}, 200
	except Exception as e:
		return {'message': str(e)}, 404
	
@app.route("/api/v1/database", methods=['GET'])
def showDatabase():
	"""
	This can be used to get all the licenses from database
	"""
	try:
		response = dB.getAll()
		df = pd.DataFrame(response)
		return render_template('database.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
	except Exception as e:
		return {'message': str(e)}, 404

@app.route("/")
def start():
	return redirect(url_for('docs'))

@app.route("/api/v1/docs")
def docs():
	return auto_doc.html(title='Flask License Manager API Documentation', author='Yash Jain'), 200

@app.route("/health")
def health():
	return 'OK', 200

@app.errorhandler(Exception)
def page_not_found(e):
		try:
			return {'message': str(e)}, e.code
		except:
			return {'message': str(e)}, 500

@app.before_request
def only_json():
		if not request.is_json and not request.path in ['/', '/api/v1/docs', '/api/v1/database', '/static/style.css', '/health']:
				abort(406, 'This server only accepts JSON')
