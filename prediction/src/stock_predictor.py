import os
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import ParameterGrid
import logging

class StockDataPreprocessor:
    def __init__(self, ticker, start_date, end_date, lookback=30):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.lookback = lookback
        self.feature_cols = ['Open', 'High', 'Low', 'Close', 'Volume',
                           'sma20', 'sma50', 'rsi', 'macd', 'signal',
                           'bb_upper', 'bb_lower', 'atr', 'stoch_k', 'stoch_d',
                           'obv', 'vwap']
        self.target_col = 'Close'
        self.feature_scaler = None
        self.target_scaler = None
        
    def load_data(self):
        """Load and preprocess stock data"""
        df = yf.download(self.ticker, self.start_date, self.end_date, interval='1d')
        if df.empty:
            raise ValueError(f"No data found for ticker {self.ticker}")
        
        df.dropna(inplace=True)
        return self._add_technical_indicators(df)
    
    def _add_technical_indicators(self, df):
        """Add technical indicators to the dataframe"""
        df = df.copy()
        
        # Moving Averages
        df['sma20'] = df['Close'].rolling(window=20).mean()
        df['sma50'] = df['Close'].rolling(window=50).mean()
        
        # Bollinger Bands
        bb_period = 20
        bb_std = df['Close'].rolling(window=bb_period).std()
        df['bb_upper'] = df['Close'].rolling(window=bb_period).mean() + (bb_std * 2)
        df['bb_lower'] = df['Close'].rolling(window=bb_period).mean() - (bb_std * 2)
        
        # Average True Range (ATR)
        high_low = df['High'] - df['Low']
        high_close = abs(df['High'] - df['Close'].shift())
        low_close = abs(df['Low'] - df['Close'].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = true_range.rolling(window=14).mean()
        
        # Stochastic Oscillator
        low_min = df['Low'].rolling(window=14).min()
        high_max = df['High'].rolling(window=14).max()
        df['stoch_k'] = ((df['Close'] - low_min) / (high_max - low_min)) * 100
        df['stoch_d'] = df['stoch_k'].rolling(window=3).mean()
        
        # On-Balance Volume (OBV)
        df['obv'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
        
        # Volume Weighted Average Price (VWAP)
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        df['vwap'] = (typical_price * df['Volume']).cumsum() / df['Volume'].cumsum()
        
        # RSI
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        
        # Normalize indicators
        for col in ['macd', 'signal', 'obv', 'atr']:
            if df[col].std() != 0:  # Avoid division by zero
                df[col] = (df[col] - df[col].mean()) / df[col].std()
        
        df.dropna(inplace=True)
        return df
    
    def prepare_data(self, df):
        """Scale data and create sequences"""
        df = df.dropna()
        
        # Initialize scalers if not already done
        if self.feature_scaler is None:
            self.feature_scaler = MinMaxScaler()
            self.target_scaler = MinMaxScaler()
        
        # Scale features
        features = df[self.feature_cols].values
        scaled_features = self.feature_scaler.fit_transform(features)
        
        # Scale target separately
        target = df[self.target_col].values.reshape(-1, 1)
        scaled_target = self.target_scaler.fit_transform(target)
        
        # Create sequences
        X, y = self._create_sequences(scaled_features, scaled_target)
        
        # Split into train and test sets (80-20 split)
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        return X_train, X_test, y_train, y_test
    
    def _create_sequences(self, features, target):
        """Create sequences for LSTM"""
        X_list, y_list = [], []
        for i in range(len(features) - self.lookback):
            X_list.append(features[i:i+self.lookback])
            y_list.append(target[i+self.lookback])
        return np.array(X_list), np.array(y_list)

class StockPredictor:
    def __init__(self, ticker, start_date='2024-01-01', end_date='2024-12-29', lookback=30):
        self.ticker = ticker
        self.model_path = f'models/{ticker}_model.keras'
        self.preprocessor = StockDataPreprocessor(ticker, start_date, end_date, lookback)
        self.model = None
        self.best_params = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _create_model(self, params):
        """Create LSTM model with given parameters"""
        model = Sequential()
        
        # First LSTM layer
        model.add(LSTM(params['lstm_units_1'], 
                      activation=params['activation'],
                      return_sequences=True,
                      input_shape=(self.preprocessor.lookback, len(self.preprocessor.feature_cols))))
        model.add(Dropout(params['dropout_1']))
        
        # Second LSTM layer
        model.add(LSTM(params['lstm_units_2'],
                      activation=params['activation'],
                      return_sequences=True))
        model.add(Dropout(params['dropout_2']))
        
        # Third LSTM layer
        model.add(LSTM(params['lstm_units_3'],
                      activation=params['activation']))
        model.add(Dropout(params['dropout_3']))
        
        # Dense layers
        model.add(Dense(params['dense_units'], activation='relu'))
        model.add(Dense(1, activation='linear'))
        
        optimizer = Adam(learning_rate=params['learning_rate'])
        model.compile(optimizer=optimizer, loss=params['loss'])
        
        return model
    
    def _grid_search(self, X_train, y_train, X_test, y_test):
        """Perform grid search for hyperparameter tuning"""
        param_grid = {
            'lstm_units_1': [64],
            'lstm_units_2': [32],
            'lstm_units_3': [1],
            'dense_units': [64, 128],
            'dropout_1': [0.2, 0.3],
            'dropout_2': [0.2],
            'dropout_3': [0.2],
            'activation': ['tanh'],
            'learning_rate': [0.001],
            'loss': ['huber', 'mean_squared_error']
        }
        
        best_loss = float('inf')
        best_params = None
        best_model = None
        
        for params in ParameterGrid(param_grid):
            self.logger.info(f"Testing parameters: {params}")
            
            model = self._create_model(params)
            history = model.fit(
                X_train, y_train,
                epochs=30,
                batch_size=32,
                validation_split=0.2,
                shuffle=False,
                verbose=0,
                callbacks=[
                    tf.keras.callbacks.EarlyStopping(
                        monitor='val_loss',
                        patience=5,
                        restore_best_weights=True
                    )
                ]
            )
            
            val_loss = min(history.history['val_loss'])
            if val_loss < best_loss:
                best_loss = val_loss
                best_params = params
                best_model = model
                self.logger.info(f"New best validation loss: {best_loss}")
        
        return best_model, best_params
    
    def train(self):
        """Train the model with automatic hyperparameter tuning"""
        # Load and prepare data
        df = self.preprocessor.load_data()
        X_train, X_test, y_train, y_test = self.preprocessor.prepare_data(df)
        
        # Don't use existing model - retrain for better results
        self.logger.info("Starting hyperparameter tuning...")
        self.model, self.best_params = self._grid_search(X_train, y_train, X_test, y_test)

        self.logger.info("Final training with best parameters...")
        self.model.fit(
            X_train, y_train,
            epochs=20,
            batch_size=32,
            validation_split=0.2,
            shuffle=False,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=10,
                    restore_best_weights=True
                )
            ]
        )
        
        # Save the model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        
        # Get predictions
        predictions = self.predict(X_test)
        return predictions, self.preprocessor.target_scaler.inverse_transform(y_test)
    
    def predict(self, X):
        if self.model is None:
            if os.path.exists(self.model_path):
                self.model = load_model(self.model_path)
            else:
                raise ValueError("Model not trained yet!")
        
        predictions_scaled = self.model.predict(X)
        return self.preprocessor.target_scaler.inverse_transform(predictions_scaled)

    def get_best_params(self):
        """Return the best parameters found during training"""
        return self.best_params
