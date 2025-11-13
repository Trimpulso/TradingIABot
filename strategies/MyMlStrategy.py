"""
Estrategia de Trading con Machine Learning para Freqtrade.
Integra predicciones de ML con lógica de compra/venta.
"""

import numpy as np
import pandas as pd
from freqtrade.strategy import IStrategy, merge_informative_pair
from freqtrade.persistence import Trade
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Importar módulos personalizados
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.ml_model import MLModel, FeatureEngineer


class MyMlStrategy(IStrategy):
    """
    Estrategia de ML para Freqtrade.
    
    Combina indicadores técnicos tradicionales con predicciones de ML.
    """
    
    # Configuración de compra/venta
    INTERFACE_VERSION = 3
    
    # Minimal ROI
    minimal_roi = {
        "0": 0.10  # 10% de ganancia
    }
    
    # Stoploss
    stoploss = -0.05  # -5% máximo de pérdida
    
    # Trailing stoploss
    trailing_stop = False
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True
    
    # Tiempo de espera
    timeframe = '1h'
    
    # Ventanas de análisis
    informative_timeframe = '4h'
    
    # Parámetros optimizables
    buy_rsi = 30
    buy_rsi_enabled = True
    
    sell_rsi = 70
    sell_rsi_enabled = True
    
    ml_buy_threshold = 0.65  # Umbral de confianza para compra
    ml_sell_threshold = 0.35  # Umbral de confianza para venta
    
    ml_weight = 0.6  # Peso del ML vs indicadores técnicos
    
    # Protección contra sobreventa
    buy_protection_enabled = True
    sell_protection_enabled = True
    
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        
        # Inicializar modelo de ML
        self.ml_model = MLModel(model_type='random_forest')
        self.feature_engineer = FeatureEngineer()
        
        # Intentar cargar modelo previamente entrenado
        self.model_path = Path(__file__).parent.parent / 'models' / 'random_forest_latest.pkl'
        if self.model_path.exists():
            try:
                self.ml_model.load_model(str(self.model_path))
                print(f"✓ Modelo ML cargado desde {self.model_path}")
            except Exception as e:
                print(f"✗ Error al cargar modelo: {e}")
        else:
            print("⚠ Modelo ML no encontrado. Usando predicciones basadas en indicadores.")
    
    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Calcula indicadores técnicos y features de ML.
        
        Args:
            dataframe: DataFrame con datos OHLC
            metadata: Información de la pareja (par, timeframe)
            
        Returns:
            DataFrame con indicadores
        """
        
        # Añadir indicadores técnicos
        dataframe = self.feature_engineer.add_technical_indicators(dataframe)
        
        # RSI adicional con diferentes períodos
        for period in [14, 21]:
            delta = dataframe['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            dataframe[f'rsi_{period}'] = 100 - (100 / (1 + rs))
        
        # TEMA (Triple Exponential Moving Average)
        ema1 = dataframe['close'].ewm(span=10).mean()
        ema2 = ema1.ewm(span=10).mean()
        ema3 = ema2.ewm(span=10).mean()
        dataframe['tema'] = 3 * ema1 - 3 * ema2 + ema3
        
        # ADX (ya incluido en TA-Lib si está disponible)
        try:
            import talib
            dataframe['adx'] = talib.ADX(dataframe['high'], dataframe['low'], dataframe['close'], timeperiod=14)
        except ImportError:
            # Alternativa sin TA-Lib
            dataframe['adx'] = 50  # Valor neutral
        
        # Predicción de ML
        try:
            feature_cols = [
                'rsi_14', 'rsi_21', 'macd', 'macd_signal', 'macd_diff',
                'bb_upper', 'bb_middle', 'bb_lower', 'atr', 'volatility',
                'price_change_1h', 'price_change_4h', 'volume_change'
            ]
            
            # Obtener últimas predicciones
            if len(dataframe) > 50 and self.ml_model.is_trained:
                for i in range(max(0, len(dataframe) - 10), len(dataframe)):
                    try:
                        df_slice = dataframe.iloc[:i+1]
                        pred, probs = self.ml_model.predict(df_slice, feature_cols)
                        dataframe.loc[dataframe.index[i], 'ml_prediction'] = pred
                        dataframe.loc[dataframe.index[i], 'ml_buy_confidence'] = probs[1]
                    except:
                        pass
        except Exception as e:
            print(f"Error en predicción ML: {e}")
        
        # Valores por defecto si ML no está disponible
        dataframe['ml_prediction'] = dataframe.get('ml_prediction', 0)
        dataframe['ml_buy_confidence'] = dataframe.get('ml_buy_confidence', 0.5)
        
        return dataframe
    
    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Define las condiciones de entrada (compra).
        """
        
        conditions = []
        
        # Condición 1: Indicadores técnicos
        technical_buy = (
            (dataframe['rsi_14'] < self.buy_rsi) &  # RSI bajo
            (dataframe['rsi_21'] < self.buy_rsi) &  # RSI bajo en período más largo
            (dataframe['macd'] > dataframe['macd_signal']) &  # MACD alcista
            (dataframe['volume'] > dataframe['volume'].rolling(20).mean() * 0.8)  # Volumen decente
        )
        
        conditions.append(technical_buy)
        
        # Condición 2: ML (si está disponible)
        if self.ml_model.is_trained:
            ml_buy = dataframe['ml_buy_confidence'] > self.ml_buy_threshold
            conditions.append(ml_buy)
        
        # Combinación ponderada
        if len(conditions) == 2:
            combined = (
                (conditions[0] * (1 - self.ml_weight)) + 
                (conditions[1].astype(int) * self.ml_weight)
            ) > 0.5
        else:
            combined = conditions[0]
        
        # Protecciones
        if self.buy_protection_enabled:
            combined = combined & (
                dataframe['atr'] > 0 &  # ATR debe ser positivo
                dataframe['volatility'] < dataframe['volatility'].rolling(50).mean() * 1.5  # No demasiada volatilidad
            )
        
        dataframe.loc[combined, 'enter_long'] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Define las condiciones de salida (venta).
        """
        
        conditions = []
        
        # Condición 1: Indicadores técnicos
        technical_sell = (
            (dataframe['rsi_14'] > self.sell_rsi) |  # RSI alto
            (dataframe['macd'] < dataframe['macd_signal'])  # MACD bajista
        )
        
        conditions.append(technical_sell)
        
        # Condición 2: ML (si está disponible)
        if self.ml_model.is_trained:
            ml_sell = dataframe['ml_buy_confidence'] < self.ml_sell_threshold
            conditions.append(ml_sell)
        
        # Combinación
        if len(conditions) == 2:
            combined = (
                (conditions[0] * (1 - self.ml_weight)) + 
                (conditions[1].astype(int) * self.ml_weight)
            ) > 0.5
        else:
            combined = conditions[0]
        
        if self.sell_protection_enabled:
            # No vender si estamos en tendencia fuerte alcista
            combined = combined & (dataframe['tema'] < dataframe['close'])
        
        dataframe.loc[combined, 'exit_long'] = 1
        
        return dataframe
    
    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, **kwargs) -> float:
        """
        Calcula un stoploss dinámico basado en ATR.
        """
        
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        
        if len(dataframe) < 2:
            return self.stoploss
        
        latest = dataframe.iloc[-1]
        
        # Stoploss dinámico: entry_price - (ATR * 2)
        if hasattr(trade, 'open_rate'):
            atr_multiplier = 2.0
            dynamic_stoploss = (latest['atr'] * atr_multiplier) / current_rate
            
            return max(-0.10, -dynamic_stoploss)  # Mínimo -10%
        
        return self.stoploss
    
    def leverage(self, pair: str, stake_amount: float, leverage_tier, **kwargs) -> float:
        """
        Define el apalancamiento (si se usa en modo de futuros).
        """
        return 1.0  # Sin apalancamiento
