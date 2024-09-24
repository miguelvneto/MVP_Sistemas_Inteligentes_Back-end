from marshmallow import Schema, fields, ValidationError

class PredictSchema(Schema):
    MALE = fields.Integer(required=True)
    AGE = fields.Integer(required=True)
    SMOKING = fields.Integer(required=True)
    YELLOW_FINGERS = fields.Integer(required=True)
    ANXIETY = fields.Integer(required=True)
    PEER_PRESSURE = fields.Integer(required=True)
    CHRONIC_DISEASE = fields.Integer(required=True)
    FATIGUE = fields.Integer(required=True)
    ALLERGY = fields.Integer(required=True)
    WHEEZING = fields.Integer(required=True)
    ALCOHOL_CONSUMING = fields.Integer(required=True)
    COUGHING = fields.Integer(required=True)
    SHORTNESS_OF_BREATH = fields.Integer(required=True)
    SWALLOWING_DIFFICULTY = fields.Integer(required=True)
    CHEST_PAIN = fields.Integer(required=True)
