from marshmallow import Schema, fields, ValidationError

class PredictSchema(Schema):
    gender = fields.Integer(required=True)
    age = fields.Integer(required=True)
    smoking = fields.Integer(required=True)
    yellow_fingers = fields.Integer(required=True)
    anxiety = fields.Integer(required=True)
    peer_pressure = fields.Integer(required=True)
    chronic_disease = fields.Integer(required=True)
    fatigue = fields.Integer(required=True)
    allergy = fields.Integer(required=True)
    wheezing = fields.Integer(required=True)
    alcohol_consuming = fields.Integer(required=True)
    coughing = fields.Integer(required=True)
    shortness_of_breath = fields.Integer(required=True)
    swallowing_difficulty = fields.Integer(required=True)
    chest_pain = fields.Integer(required=True)
