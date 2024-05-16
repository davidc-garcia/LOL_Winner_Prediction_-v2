from flask import Flask, jsonify, request
from loguru import logger
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import requests
import tempfile

app = Flask(__name__)

@app.route("/")
def install():
    return """
    INSTALLING WINDOWS XP
    ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▢
    　　╭━╮╭━╮╭╮  ╱
    　　╰━┫╰━┫╰╯ ╱╭╮
    　　╰━╯╰━╯  ╱ ╰╯
　　　　　　　　　     COMPLETE
    """
# Defino la función predict
def predict(model, x_test, threshold=0.5):
    proba = model.predict_proba(x_test[['dominant score']])
    y_pred = (proba[:, 1] > threshold).astype(int)
    return y_pred

# Función para realizar predicciones
def predict_v2(model, data):
    # Crea un DataFrame a partir de los datos
    df = pd.DataFrame([data])
    
    # Realiza la predicción utilizando el modelo
    proba = model.predict_proba(df[['dominant score']])
    prediction = (proba[:, 1] > 0.5).astype(int)  # Suponiendo un umbral de 0.5
    
    return prediction.tolist()

# Defino la ruta para recibir los archivos CSV y PKL como entradas
@app.route("/predict", methods=['POST'])
def make_prediction(): 
    # Verificar si se subieron los archivos
    if 'input_file' not in request.files or 'model_file' not in request.files:
        return jsonify({"error": "Both input file and model file are required."}), 400
    
    input_file = request.files['input_file']
    model_file = request.files['model_file']

    # Crear un archivo temporal para guardar el archivo de modelo
    with tempfile.NamedTemporaryFile(delete=False) as temp_model_file:
        model_file.save(temp_model_file.name)

        # Leer el archivo de modelo
        model = pickle.load(open(temp_model_file.name, 'rb'))

    # Leer los datos de entrada
    input_data = pd.read_csv(input_file)

    try:
        logger.info("Making predictions")
        # Realizar predicciones
        predictions = predict(model, input_data)
        return jsonify({"predictions": predictions.tolist()}), 200
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500


#Método de entrenamiento
@app.route("/train", methods=['POST'])
def train_model():
    # Verificar si se subieron los archivos
    if 'data_file' not in request.files:
        return jsonify({"error": "Data file is required."}), 400
    
    data_file = request.files['data_file']
    
    # Cargar datos de entrenamiento
    df = pd.read_csv(data_file, header=0)
    Xtr = df[['dominant score']]  # Utilizar solo la columna 'dominant score' como característica
    ytr = df['win_adj']  # Etiquetas

    # Entrenar modelo
    model = RandomForestClassifier()
    model.fit(Xtr, ytr)

    # Guardar modelo
    model_filename = 'model2.pkl'  # Define la ruta del archivo del modelo
    with open(model_filename, "wb") as f:
        pickle.dump(model, f)

    return jsonify({"message": "Model trained and saved successfully model2.pkl"}), 200


# Ruta para realizar predicciones sin archivo csv, con una lista
@app.route("/predict_v2", methods=['POST'])
def make_prediction_v2(): 
    data = request.json
    model_file = 'model.pkl'  # Ruta del archivo del modelo

    # Cargar el modelo
    with open(model_file, 'rb') as f:
        model = pickle.load(f)

    try:
        logger.info("Making predictions")
        # Realizar predicciones utilizando los datos proporcionados
        predictions = predict_v2(model, data)
        return jsonify({"predictions": predictions}), 200
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Configurar la carpeta de carga para almacenar temporalmente los archivos subidos
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run(debug=True)