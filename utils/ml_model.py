"""
Módulo de Machine Learning para predicciones de trading.
Incluye entrenamiento, predicción y manejo de modelos.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import os
from datetime import datetime
from pathlib import Path


class MLModel:
    """Clase para gestionar modelos de ML para trading."""
    
    def __init__(self, model_type='random_forest', model_path='models/'):
        """
        Inicializa el modelo de ML.
        
        Args:
            model_type: 'random_forest' o 'gradient_boosting'
            model_path: ruta donde guardar/cargar modelos
        """
        self.model_type = model_type
        self.model_path = Path(model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = None
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Inicializa el modelo según el tipo especificado."""
        if self.model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                random_state=42,
                n_jobs=-1,
                min_samples_split=10,
                min_samples_leaf=5
            )
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
                subsample=0.8
            )
        else:
            raise ValueError(f"Tipo de modelo no soportado: {self.model_type}")
    
    def prepare_features(self, df: pd.DataFrame, feature_cols: list) -> np.ndarray:
        """
        Prepara y normaliza las características.
        
        Args:
            df: DataFrame con los datos
            feature_cols: lista de columnas a usar como features
            
        Returns:
            Array normalizado
        """
        self.feature_names = feature_cols
        X = df[feature_cols].values
        
        if not self.is_trained:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def create_target(self, df: pd.DataFrame, threshold: float = 0.01) -> np.ndarray:
        """
        Crea etiquetas objetivo basadas en cambios de precio.
        
        Args:
            df: DataFrame con datos OHLC
            threshold: umbral de cambio (1% por defecto)
            
        Returns:
            Array de etiquetas (1 = compra, 0 = venta/esperar)
        """
        price_change = (df['close'].shift(-1) - df['close']) / df['close']
        target = (price_change > threshold).astype(int)
        return target[:-1].values  # Remove last NaN
    
    def train(self, df: pd.DataFrame, feature_cols: list, threshold: float = 0.01, 
              test_size: float = 0.2) -> dict:
        """
        Entrena el modelo con datos históricos.
        
        Args:
            df: DataFrame con datos históricos
            feature_cols: columnas a usar como features
            threshold: umbral de cambio para determinar compra/venta
            test_size: proporción de datos de prueba
            
        Returns:
            Diccionario con métricas de desempeño
        """
        X = self.prepare_features(df, feature_cols)
        y = self.create_target(df, threshold)
        
        # Asegurar que X e y tienen la misma longitud
        min_len = min(len(X), len(y))
        X = X[:min_len]
        y = y[:min_len]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluación
        y_pred = self.model.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'train_size': len(X_train),
            'test_size': len(X_test)
        }
        
        return metrics
    
    def predict(self, df: pd.DataFrame, feature_cols: list) -> tuple:
        """
        Realiza predicciones sobre nuevos datos.
        
        Args:
            df: DataFrame con datos recientes
            feature_cols: columnas a usar como features
            
        Returns:
            Tupla (predicción_binaria, probabilidad)
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado aún")
        
        X = self.prepare_features(df, feature_cols)
        
        prediction = self.model.predict(X[-1:])
        probabilities = self.model.predict_proba(X[-1:])
        
        return prediction[0], probabilities[0]
    
    def save_model(self, name: str = None) -> str:
        """
        Guarda el modelo entrenado.
        
        Args:
            name: nombre del archivo (sin extensión)
            
        Returns:
            Ruta donde se guardó el modelo
        """
        if not self.is_trained:
            raise ValueError("No hay modelo entrenado para guardar")
        
        if name is None:
            name = f"{self.model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        model_file = self.model_path / f"{name}.pkl"
        scaler_file = self.model_path / f"{name}_scaler.pkl"
        
        with open(model_file, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(scaler_file, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        return str(model_file)
    
    def load_model(self, model_file: str):
        """
        Carga un modelo previamente entrenado.
        
        Args:
            model_file: ruta del archivo del modelo
        """
        model_file = Path(model_file)
        scaler_file = model_file.parent / f"{model_file.stem}_scaler.pkl"
        
        if not model_file.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {model_file}")
        
        with open(model_file, 'rb') as f:
            self.model = pickle.load(f)
        
        if scaler_file.exists():
            with open(scaler_file, 'rb') as f:
                self.scaler = pickle.load(f)
        
        self.is_trained = True


class FeatureEngineer:
    """Clase para ingeniería de características."""
    
    @staticmethod
    def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Añade indicadores técnicos al DataFrame.
        
        Args:
            df: DataFrame con datos OHLC
            
        Returns:
            DataFrame con indicadores adicionales
        """
        df = df.copy()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        ema_12 = df['close'].ewm(span=12).mean()
        ema_26 = df['close'].ewm(span=26).mean()
        df['macd'] = ema_12 - ema_26
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_diff'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        sma = df['close'].rolling(window=20).mean()
        std = df['close'].rolling(window=20).std()
        df['bb_upper'] = sma + (std * 2)
        df['bb_lower'] = sma - (std * 2)
        df['bb_middle'] = sma
        
        # ATR (Average True Range)
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = tr.rolling(window=14).mean()
        
        # Volatility
        df['volatility'] = df['close'].rolling(window=20).std()
        
        # Price changes
        df['price_change_1h'] = df['close'].pct_change(1) * 100
        df['price_change_4h'] = df['close'].pct_change(4) * 100
        
        # Volume-related
        df['volume_change'] = df['volume'].pct_change(1)
        
        return df.dropna()
