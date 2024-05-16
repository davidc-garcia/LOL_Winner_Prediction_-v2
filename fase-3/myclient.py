import os
import requests

# Función para hacer solicitudes GET a la raíz del servidor Flask
def get_root_response():
    root_endpoint = 'http://localhost:5000/'
    response = requests.get(root_endpoint)
    print("Response:", response.text)

# Función para hacer solicitudes POST al servidor Flask para predicciones
def make_prediction_request():
    # Dirección del servidor Flask para predicciones
    server_url = 'http://localhost:5000/predict'

    # Rutas de los archivos CSV y PKL
    path = os.path.join(os.getcwd())
    input_file_path = os.path.join(path, 'test_data_input.csv')
    model_file_path = os.path.join(path, 'model.pkl')

    # Verificar si los archivos existen
    if not os.path.isfile(input_file_path) or not os.path.isfile(model_file_path):
        print("Input file or model file not found.")
        return

    # Cargar los archivos en un diccionario para enviarlos con requests
    files = {
        'input_file': open(input_file_path, 'rb'),
        'model_file': open(model_file_path, 'rb')
    }

    # Hacer la solicitud POST al servidor Flask
    response = requests.post(server_url, files=files)

    # Verificar la respuesta del servidor
    if response.status_code == 200:
        data = response.json()
        predictions = data.get('predictions')
        print("Predictions:", predictions)
    else:
        print("Error:", response.text)

# Función para hacer solicitudes POST al servidor Flask para entrenar el modelo
def train_model():
    train_endpoint = 'http://localhost:5000/train'  # Reemplaza esto con la URL correcta de tu servidor Flask
    data_file_path = 'train_data.csv'  # Ruta al archivo CSV de datos de entrenamiento

    # Verificar si el archivo de datos de entrenamiento existe
    if not os.path.isfile(data_file_path):
        print("Training data file not found.")
        return

    # Cargar el archivo CSV
    with open(data_file_path, 'rb') as data_file:
        files = {'data_file': data_file}
        response = requests.post(train_endpoint, files=files)

    print("Train response:", response.text)

# Función para hacer solicitudes POST al servidor Flask para predicciones (nuevo método predict_v2)
def make_prediction_v2_request():
    # URL del servidor Flask donde está desplegado el nuevo método predict_v2
    predict_v2_endpoint = 'http://localhost:5000/predict_v2'

    # Datos de predicción en el formato esperado por el servidor
    prediction_data_1 = {
        'matchup': 'Caitlyn vs Tristana',
        'dominant score': 50.98152424942263
    }

    prediction_data_2 = {
        'matchup': 'Lee Sin vs Sejuani',
        'dominant score': 47.69736842105263
    }

    # Realizar la solicitud POST al servidor para el primer conjunto de datos de predicción
    response1 = requests.post(predict_v2_endpoint, json=prediction_data_1)

    # Realizar la solicitud POST al servidor para el segundo conjunto de datos de predicción
    response2 = requests.post(predict_v2_endpoint, json=prediction_data_2)

    # Imprimir las respuestas del servidor
    print("Respuesta 1:", response1.json())
    print("Respuesta 2:", response2.json())

# Llamar a las funciones para ejecutar las solicitudes
print("Solicitud a /")
get_root_response()
print("Solicitud a predict con CSV")
make_prediction_request()
print("Solicitud a predict_v2 con datos en diccionarios")
make_prediction_v2_request()
print("Solicitud a train, por favor espere")
train_model()

