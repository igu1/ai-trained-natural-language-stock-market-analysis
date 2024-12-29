import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

def load_trained_model(model_path: str):
    """
    Loads a trained Keras model from disk.
    """
    return load_model(model_path)

def predict(model, X: pd.DataFrame) -> np.ndarray:
    """
    Generates predictions using the loaded model.
    """
    return model.predict(X)
