# API de Predição de Câncer de Pulmão

## Visão Geral

A **API de Predição de Câncer de Pulmão** permite que os usuários prevejam a probabilidade de câncer de pulmão com base em diversos fatores de saúde e estilo de vida. A predição é feita utilizando um modelo de machine learning pré-treinado. Este arquivo README explica como configurar, executar e interagir com a API.

## Tecnologias Utilizadas

- Python
- Flask
- Flask-OpenAPI3
- Pandas
- Pickle
- Marshmallow (para validação de esquemas)
- Flask-CORS (para Cross-Origin Resource Sharing)

## Funcionalidades

- **Predição de Câncer de Pulmão**: Envie dados de saúde e estilo de vida para a API e receba uma predição sobre a probabilidade de câncer de pulmão.
- **Documentação OpenAPI3**: A API fornece documentação interativa para testar os endpoints.

## Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- Pip (gerenciador de pacotes Python)

### Passo a Passo de Instalação

1. **Clone o repositório**:
   ```bash
   git clone <https://github.com/miguelvneto/MVP_Sistemas_Inteligentes_Back-end.git>
   cd lung-cancer-prediction-api
   ```

2. **Prepare o Ambiente Virtual (opcional)**:
    ```bash
    python -m venv myenv
    myenv/Scripts/activate
    ```
3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Defina a variável de ambiente para o pipeline**:
   Certifique-se de que o caminho para o modelo de predição de câncer de pulmão está correto. Você pode definir a variável de ambiente `PIPELINE_PATH` ou colocar o modelo no caminho padrão (`pipeline/lung_cancer_prediction-pipeline.pkl`).

   Se estiver usando variáveis de ambiente:
   ```bash
   export PIPELINE_PATH="caminho/para/seu/lung_cancer_prediction-pipeline.pkl"
   ```

5. **Execute o servidor Flask**:
   ```bash
   python app.py
   ```

6. **Acesse a documentação da API**:
   Após executar o servidor, vá para `http://localhost:5000/openapi` para acessar a documentação interativa da API.

## Endpoints da API

### URL Base

A URL base para a API é:

```
http://localhost:5000/
```

### `/`

**Método**: `GET`

**Descrição**: Redireciona para a documentação OpenAPI.

---

### `/predict`

**Método**: `POST`

**Descrição**: Realiza a predição de câncer de pulmão com base nos dados de saúde e estilo de vida.

#### Esquema do Corpo da Requisição

- `gender` (string): Gênero do paciente, deve ser 'm' (masculino) ou 'f' (feminino).
- `age` (inteiro): Idade do paciente, deve ser um número inteiro positivo.
- `smoking` (string): Hábito de fumar, deve ser 'y' (sim) ou 'n' (não).
- `yellow_fingers` (string): O paciente tem dedos amarelados? Deve ser 'y' (sim) ou 'n' (não).
- `anxiety` (string): O paciente sofre de ansiedade? Deve ser 'y' (sim) ou 'n' (não).
- `peer_pressure` (string): O paciente sofre pressão social? Deve ser 'y' (sim) ou 'n' (não).
- `chronic_disease` (string): O paciente tem doenças crônicas? Deve ser 'y' (sim) ou 'n' (não).
- `fatigue` (string): O paciente sente fadiga? Deve ser 'y' (sim) ou 'n' (não).
- `allergy` (string): O paciente tem alergias? Deve ser 'y' (sim) ou 'n' (não).
- `wheezing` (string): O paciente tem chiado no peito? Deve ser 'y' (sim) ou 'n' (não).
- `alcohol_consuming` (string): O paciente consome álcool? Deve ser 'y' (sim) ou 'n' (não).
- `coughing` (string): O paciente tem tosse persistente? Deve ser 'y' (sim) ou 'n' (não).
- `shortness_of_breath` (string): O paciente tem falta de ar? Deve ser 'y' (sim) ou 'n' (não).
- `swallowing_difficulty` (string): O paciente tem dificuldade para engolir? Deve ser 'y' (sim) ou 'n' (não).
- `chest_pain` (string): O paciente sente dor no peito? Deve ser 'y' (sim) ou 'n' (não).

#### Exemplo de Requisição

```json
{
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
```

#### Respostas

- **Sucesso**: `200 OK`
  
  ```json
  {
      "message": "Predição realizada com sucesso",
      "result": "Alta probabilidade de Câncer de Pulmão.",
      "cancer": "YES"
  }
  ```

- **Erro de Validação**: `400 Bad Request`

  Exemplo:
  
  ```json
  {
      "error": {
          "age": "O campo 'age' deve ser um número inteiro positivo.",
          "smoking": "O campo 'smoking' deve ser 'y' (sim) ou 'n' (não)."
      }
  }
  ```

- **Erro de Predição**: `500 Internal Server Error`

  ```json
  {
      "error": "Erro na predição: <detalhes-do-erro>"
  }
  ```

## Deploy

1. Certifique-se de que a variável de ambiente `PIPELINE_PATH` está definida corretamente para o caminho do modelo.
2. A API pode ser implantada em qualquer plataforma que suporte aplicações Flask (por exemplo, Heroku, AWS Elastic Beanstalk).