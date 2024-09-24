from flask import jsonify, redirect
from flask_openapi3 import OpenAPI, Info, Tag
from flask_openapi3.models import BaseModel
from models.PredictSchema import PredictSchema
from marshmallow import ValidationError
import pickle
import pandas as pd
from flask_cors import CORS
import os

# Informações sobre a API
info = Info(title="Lung Cancer Prediction API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Carregando o pipeline de predição
pipeline_path = os.getenv('PIPELINE_PATH', 'pipeline/lung_cancer_prediction-pipeline.pkl')
with open(pipeline_path, 'rb') as pipeline_file:
    pipeline = pickle.load(pipeline_file)

# Função para validar os dados de entrada
def validar_entrada(data):
    error_messages = {}

    # Validação para gender: deve ser 'm' ou 'f'
    if data['gender'] not in ['m', 'f']:
        error_messages['gender'] = "The field 'gender' must be 'm' (male) or 'f' (female)."

    # Validação para age: deve ser um inteiro positivo
    if not isinstance(data['age'], int) or data['age'] <= 0:
        error_messages['age'] = "The field 'age' must be a positive integer."

    # Validação para todos os outros campos: devem ser 'y' ou 'n'
    for key in ['smoking', 'yellow_fingers', 'anxiety', 'peer_pressure', 'chronic_disease', 'fatigue',
                'allergy', 'wheezing', 'alcohol_consuming', 'coughing', 'shortness_of_breath', 
                'swallowing_difficulty', 'chest_pain']:
        if data[key] not in ['y', 'n']:
            error_messages[key] = f"The field '{key}' must be 'y' (yes) or 'n' (no)."

    return error_messages

# Função para fazer a conversão para o padrão da base de dados
def padroniza(d):
    for key, value in d.items():
        if isinstance(value, str):
            if value.lower() in ['n', 'f']:  # Convertendo 'n' ou 'f' para 1
                d[key] = 1
            elif value.lower() in ['y', 'm']:  # Convertendo 'y' ou 'm' para 2
                d[key] = 2
    return d

# Inicialização do esquema de validação
schema = PredictSchema()

# Definindo o modelo de entrada para o OpenAPI3 usando Pydantic
class PredictionInput(BaseModel):
    gender: str
    age: int
    smoking: str
    yellow_fingers: str
    anxiety: str
    peer_pressure: str
    chronic_disease: str
    fatigue: str
    allergy: str
    wheezing: str
    alcohol_consuming: str
    coughing: str
    shortness_of_breath: str
    swallowing_difficulty: str
    chest_pain: str

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "gender": "m",
                "age": 50,
                "smoking": "y",
                "yellow_fingers": "n",
                "anxiety": "n",
                "peer_pressure": "y",
                "chronic_disease": "n",
                "fatigue": "n",
                "allergy": "y",
                "wheezing": "n",
                "alcohol_consuming": "y",
                "coughing": "n",
                "shortness_of_breath": "y",
                "swallowing_difficulty": "n",
                "chest_pain": "y"
            }
        }

# Criando a tag para organizar as operações da API
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
predict_tag = Tag(name="Predição", description="Operações relacionadas à predição de câncer de pulmão")

# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

@app.post('/predict', tags=[predict_tag])
def predict(body: PredictionInput):
    """Realiza a predição de câncer de pulmão com base nos dados fornecidos"""
    json_data = body.model_dump()

    # Validação personalizada dos dados recebidos
    error_messages = validar_entrada(json_data)
    if error_messages:
        return jsonify({'error': error_messages}), 400

    # Padronizar os valores para o formato esperado pelo pipeline
    json_padronizado = padroniza(json_data)
    
    try:
        # Carrega os parametros
        data = schema.load(json_padronizado)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    df = pd.DataFrame([data])

    if pipeline:
        try:
            # Realizando a previsão com o pipeline
            prediction = pipeline.predict(df)

            # Interpretação da predição
            result = "Alta probabilidade de Câncer de Pulmão." if prediction[0] == 'YES' else "Baixa probabilidade de Câncer de Pulmão."
            cancer = prediction[0]

        except Exception as e:
            return jsonify({'error': f'Erro na predição: {str(e)}'}), 500

        return jsonify({
            'message': 'Predição realizada com sucesso',
            'result': result,
            'cancer': cancer
        }), 200
    else:
        return jsonify({'error': 'Pipeline não carregado.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
