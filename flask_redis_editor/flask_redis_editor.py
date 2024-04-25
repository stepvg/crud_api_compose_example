# -*- coding: utf-8 -*-
#! /usr/bin/python3

# pip install python-dotenv redis flask gevent

import logging, pathlib, argparse, os, dotenv, flask, redis

dotenv.load_dotenv()

app_name = pathlib.Path(__file__).stem

logging_format = f"%(asctime)s [%(levelname)s:%(name)s] - %(message)s -> %(pathname)s, line %(lineno)d, in %(funcName)s"
logger = logging.getLogger(app_name)

# connect to redis
db = redis.Redis(os.getenv('REDIS_HOST'), os.environ['REDIS_PORT'], password=os.getenv('REDIS_PASSWORD'))
	# decode_responses=True,										# automatically convert responses from bytes to strings

app = flask.Flask(app_name)											# creating flask application
if app.debug:
	logging.basicConfig( level=logging.DEBUG, format=logging_format)		# Logging configuration

@app.put("/<path:key>")
def put_item(key):
	db[key] = flask.request.get_data()
	logger.debug(f'PUT {key} -> {db[key]}')
	return b'', 204												# return no response body

@app.post("/<path:key>")
def post_item(key):
	if key in db:
		msg = {'error': 'The resource already exists!'}
		logger.debug(f'POST {key} -> {msg}')
		return msg, 409
	db[key] = flask.request.get_data()
	logger.debug(f'POST {key} -> {db[key]}')
	# For 201 (Created) responses, the Location value refers to the primary resource created by the request.
	return {"msg": "Created Successfully"}, 201, {'Location': flask.request.base_url}

@app.get("/<path:key>")
def get_item(key):
	try:
		logger.debug(f'GET {key} -> {db[key]}')
		return db[key]
	except KeyError:
		logger.debug(f'GET {key} -> ERROR The resource is not exists!')
		flask.abort(404)


if __name__ == "__main__":
	# flask --app flask_redis_editor.py run --port $FLASK_PORT --host=$FLASK_HOST
	#~ app.run(host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))
	from gevent.pywsgi import WSGIServer								# For production
	http_server = WSGIServer((os.getenv('FLASK_HOST'), int(os.getenv('FLASK_PORT'))), app)
	try:
		http_server.serve_forever()
	except KeyboardInterrupt:
		http_server.stop()
