import argparse
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from loguru import logger
import os
import pandas as pd
import pickle

# Define la función predict
def predict(model, x_test, threshold=0.5):
    # Obtener las probabilidades estimadas de cada clase para cada instancia de prueba
    proba = model.predict_proba(x_test[['dominant score']])
    
    # Predicción basada en el umbral
    y_pred = np.where(proba[:, 1] > threshold, 1, 0)
    
    return y_pred

parser = argparse.ArgumentParser()
parser.add_argument('--input_file', required=True, type=str, help='a csv file with input data (no targets)')
parser.add_argument('--predictions_file', required=True, type=str, help='a csv file where predictions will be saved to')
parser.add_argument('--model_file', required=True, type=str, help='a pkl file with a model already stored (see train.py)')

args = parser.parse_args()

model_file       = args.model_file
input_file        = args.input_file
predictions_file = args.predictions_file

if not os.path.isfile(model_file):
    logger.error(f"model file {model_file} does not exist")
    exit(-1)

if not os.path.isfile(input_file):
    logger.error(f"input file {input_file} does not exist")
    exit(-1)
    
    
logger.info("loading input data")
Xts = pd.read_csv(input_file)


logger.info("loading model")
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
    
logger.info("making predictions")
preds = predict(model, Xts)

logger.info(f"saving predictions to {predictions_file}")
pd.DataFrame(preds.reshape(-1,1), columns=['preds']).to_csv(predictions_file, index=False)
