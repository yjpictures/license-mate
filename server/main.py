from flask import Flask, redirect, url_for, request, abort, render_template
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from database import MongoDB
import pandas as pd

dB = MongoDB()
dB.connect()
app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
users = {
	'admin': generate_password_hash(dB.adminPWD),
	'manager': generate_password_hash(dB.managerPWD),
	'client': generate_password_hash(dB.clientPWD)
}

@auth.verify_password
def verifyPassword(username, password):
	if username in users and check_password_hash(users.get(username), password):
		return username
	elif username not in users:
		abort(404, 'Not a valid user')
	elif not check_password_hash(users.get(username), password):
		abort(401, 'Incorrect password')
	
@auth.get_user_roles
def getUserRoles(user):
	return user

@auth.error_handler
def authError(status):
	return {'message': 'User does not have access privileges'}, status

@app.route("/api/v1/create", methods=['POST'])
@auth.login_required(role=['manager', 'admin'])
def create():
	"""
	This can be used to create a new license.
	Authorized access: 'manager', 'admin'
	"""
	try:
		response = dB.create(request.get_json())
		return {'message': 'Created a new license', '_id': response}, 200
	except Exception as e:
		return {'message': str(e)}, 400

@app.route("/api/v1/renew", methods=['PATCH'])
@auth.login_required(role=['manager', 'admin'])
def renew():
	"""
	This can be used to renew a license.
	Authorized access: 'manager', 'admin'
	"""
	try:
		dB.renew(request.get_json())
		return {'message': 'Renewed the license'}, 200
	except Exception as e:
		return {'message': str(e)}, 404

@app.route("/api/v1/delete", methods=['DELETE'])
@auth.login_required(role=['manager', 'admin'])
def delete():
	"""
	This can be used to delete a license.
	Authorized access: 'manager', 'admin'
	"""
	try:
		dB.delete(request.args.to_dict())
		return {'message': 'Deleted the license'}, 200
	except Exception as e:
		return {'message': str(e)}, 404

@app.route("/api/v1/validate", methods=['GET'])
@auth.login_required
def validate():
	"""
	This can be used to validate a license.
	Authorized access: 'client', 'manager', 'admin'
	"""
	try:
		response = dB.validate(request.args.to_dict())
		return {'message': 'Validated the license', 'license-details': response}, 200
	except Exception as e:
		return {'message': str(e)}, 404
	
@app.route("/api/v1/get-all", methods=['GET'])
@auth.login_required(role=['admin'])
def getAll():
	"""
	This can be used to get all the licenses from database.
	Authorized access: 'admin'
	"""
	try:
		response = dB.getAll()
		return {'license-database': response}, 200
	except Exception as e:
		return {'message': str(e)}, 404
	
@app.route("/api/v1/database", methods=['GET'])
@auth.login_required(role=['admin'])
def showDatabase():
	"""
	This can be used to get all the licenses from database.
	Authorized access: 'admin'
	"""
	try:
		response = dB.getAll()
		df = pd.DataFrame(response)
		return render_template('database.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
	except Exception as e:
		return {'message': str(e)}, 404

@app.route('/ui')
def adminUI():
	"""
	This is where user can access the server ui.
	"""
	return 'UI coming soon'

@app.route("/")
def start():
	"""
	This is for home directory. It is set to redirect to docs page.
	"""
	return redirect(url_for('docs'))

@app.route('/api/v1/docs')
def docs():
	"""
	This is where the docs are rendered.
	"""
	return render_template('docs.html')

@app.route("/healthz")
def health():
	"""
	This is for health check. Always replies 200 OK.
	"""
	return 'OK', 200

@app.errorhandler(Exception)
def handleError(e):
	"""
	This is for handing errors.
	"""
	try:
		return {'message': str(e)}, e.code
	except:
		return {'message': str(e)}, 500

@app.before_request
def onlyJSON():
	"""
	This is to make sure there is a JSON payload
	"""
	if not request.is_json and request.path in ['/api/v1/create', '/api/v1/renew']:
		abort(406, '%s requires a JSON payload' % request.path)
