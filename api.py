from flask import Flask, request, jsonify
from models.PredictSchema import PredictSchema
from marshmallow import ValidationError
import pickle
import pandas as pd
from flask_cors import CORS
import os

# Inicialização da aplicação Flask
app = Flask(__name__)
CORS(app)

# Carregando o pipeline de predição
pipeline_path = os.getenv('PIPELINE_PATH', 'pipeline/lung_cancer_prediction.pkl')
with open(pipeline_path, 'rb') as pipeline_file:
    pipeline = pickle.load(pipeline_file)
print(f"Pipeline carregado a partir de '{pipeline_path}'.")

# Inicialização do esquema de validação
schema = PredictSchema()

@app.route('/predict', methods=['POST'])
def predict():
    json_data = request.get_json()

    if not json_data:
        return jsonify({'error': 'Dados JSON não fornecidos'}), 400

    try:
        # Validação dos dados recebidos
        data = schema.load(json_data)
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
    app.run()
    