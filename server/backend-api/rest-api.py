from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import csv, os, datetime, json




app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)
cors = CORS(app, resources = {r"/co2/*":{"origins": "*"}})

class WeatherModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    temperature = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Weather(name: {name}, temperature: {temperature}, pressure: {pressure}"

#db.create_all()

data_post_args = reqparse.RequestParser()

data_post_args.add_argument("temp", type=float)
data_post_args.add_argument("pressure", type=float)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'temperature': fields.Float,
    'pressure':fields.Float
}



class MeasuredValue(Resource):
    def get(self, id):
  
        return {"csv": csv}


    def post(self,id):
        args = data_post_args.parse_args()
        now = datetime.datetime.today().isoformat("T")
        with open("./data/" + id + ".csv", mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([now, args['value']])

        return '', 201
class AvaiableSensors(Resource):
    def get(self):
        files = []
        for (_, _, filenames) in os.walk("./data/"):
            files.extend(filenames)
            break
        for i in range(0,len(files)):
            files[i] = files[i].split('.')[0]
        names_of_sensors = {"names":files}
        return names_of_sensors


api.add_resource(MeasuredValue, "/co2/<string:id>")
api.add_resource(AvaiableSensors, "/co2/overview")
if __name__ =="__main__":
    app.run(host='0.0.0.0', debug=True)




