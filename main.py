from flask import Flask, request, jsonify
import time, math
from celery_config import celery
from transformers import pipeline
from tasks import PCB_defection
from flask_cors import CORS

app = Flask("myapp")
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

celery.conf.update(app.config)

@app.route("/")
def home():
    return "Home page"


@app.route("/process",methods=["POST"]) # Ném vào redis
def process():
    data = request.get_json()
    base64_image = data.get('file')
    baseimage=repr(base64_image)[1:-1]
    task  = PCB_defection.apply_async(args=[baseimage])
    return jsonify({
        'task_id': task.id
    }), 200


@app.route("/getstatus/<task_id>") # Ném vào redis
def getstatus(task_id):
    task  = PCB_defection.AsyncResult(task_id)
    if task.ready():
        result = jsonify(task.result)
    else:
        result = "Running"
    return  jsonify(result)

@app.route("/api/callApi/<task_id>") # Send the base64-encoded image as a JSON response
def sendImage(task_id):
    task  = PCB_defection.AsyncResult(task_id)
    if task.ready():
        result = task.result
        response_data = {
            "status": "completed",
            "data": result  # assuming this is the base64-encoded image data
        }
    else:
        response_data = {
            "status": "running"
        }

    return jsonify(response_data), 200



app.run(host="localhost", port=5050)