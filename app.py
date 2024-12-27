from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import socket, os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()

username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
host = os.getenv('MONGO_HOSTNAME')
database = os.getenv('MONGO_DATABASE')
collection = os.getenv('MONGO_COLLECTION')

URI = f"mongodb://{username}:{password}@{host}/{database}"


c_connect = MongoClient(URI)
mydb = c_connect[database]
mycol = mydb[collection]

@app.route('/')
def index():
	HOST = socket.gethostname()
	IPADDR = socket.gethostbyname(HOST)
	hostinfo = { "host": HOST, "ip": IPADDR }
	return jsonify(hostinfo)

@app.route('/records')
def records():
	records_list = list(mycol.find())
	for id in records_list:
		id["_id"] = str(id["_id"])
	return records_list

@app.route('/insert',methods=['POST'])
def insert_record():
	insert_data = request.json
	brand = insert_data.get('brand')
	model = insert_data.get('model')
	inserted_record = mycol.insert_one({"brand": brand, "model": model})
	return str(inserted_record.inserted_id)

@app.route('/del/<id>')
def delete_record(id):
	deleted_record = mycol.delete_one({"_id": ObjectId(id)})
	return str(deleted_record.deleted_count)



if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=8000)
