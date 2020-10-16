from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import csv, os, datetime, json




app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)
cors = CORS(app, resources = {r"/co2/*":{"origins": "*"}})

class WeatherModel(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Weather(name: {name}, temperature: {temperature}, pressure: {pressure}, timestamp: {timestamp})"

db.create_all()

data_post_args = reqparse.RequestParser()

data_post_args.add_argument("temp", type=float)
data_post_args.add_argument("pressure", type=float)

resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'temperature': fields.Float,
    'pressure':fields.Float,
    'timestamp':fields.String
}



class MeasuredValue(Resource):
    @marshal_with(resource_fields)
    def get(self, sensor_id):
        result = WeatherModel.query.filter_by(name=sensor_id).all()
        return result

    @marshal_with(resource_fields)
    def put(self,sensor_id):
        args = data_post_args.parse_args()
        now = datetime.datetime.today().isoformat("T")
        weather_data = WeatherModel(name=sensor_id, temperature=args['temp'], pressure=args["pressure"], timestamp=now)
        db.session.add(weather_data)
        db.session.commit()
        return weather_data, 201

class AvaiableSensors(Resource):
    def get(self):
        result = WeatherModel.query.with_entities(WeatherModel.name)
        return result

api.add_resource(MeasuredValue, "/co2/<string:sensor_id>")
api.add_resource(AvaiableSensors, "/co2/overview")
if __name__ =="__main__":
    app.run(host='0.0.0.0', debug=True)




