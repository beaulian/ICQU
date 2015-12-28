# coding=utf-8

from config import *
from flask import Flask, make_response, g, request, jsonify

app = Flask(__name__)


@app.before_request
def before_request():
    g.client = MongoClient(MONGO_URI, MONGO_PORT)
    g.db = g.client[MONGO_DB]
    g.coll = g.db[COLLECTION_NAME] 


@app.teardown_request
def teardown_request(exception=None):
    g.client.close()


@app.route("/remind", methods=["POST"])
def remind():
	email = request.form.get("email", False)
	if not email:
		return jsonify({"errcode": 1, "errmsg": "no email"})
	time_interval = request.form.get("time", 21600)
	g.coll.insert({"email": email, "time_interval": time_interval})
	return jsonify({"errcode": 0})