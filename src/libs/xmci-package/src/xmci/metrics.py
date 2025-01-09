from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import numpy as np
from datetime import timedelta, datetime
from enum import Enum, auto

class MetricType(Enum):
    SERVICE_FACTOR = auto()
    OP_SATURATION = auto()
    PV_SATURATION = auto()
    INTEGRAL_ABSOLUTE_ERROR = auto()
    ERROR_STANDARD_DEVIATION = auto()
    ERROR_MAXIMUM = auto()
    SETPOINT_CROSSINGS = auto()
    VALVE_TRAVEL = auto()
    VALVE_REVERSALS = auto()

class ControllerStatus(Enum):
    NORMAL = auto()
    MANUAL_CONTROL = auto()
    OUT_OF_SERVICE = auto()
    INSTRUMENT_RANGE = auto()
    VALVE_SIZING = auto()
    POOR_TUNING = auto()
    AGGRESSIVE_TUNING = auto()
    VALVE_WEAR = auto()

class Metric(ABC):
    @abstractmethod
    def calculate(self, data: Dict[str, np.ndarray], config: Dict[str, Any]) -> float:
        pass

class ServiceFactor(Metric):
    def calculate(self, data: Dict[str, np.ndarray], config: Dict[str, Any]) -> float:
        auto_mode = config.get('auto_mode', 1)
        return np.mean(np.array(data['mode']) == auto_mode) * 100

class Saturation(Metric):
    def __init__(self, saturation_type: str):
        if saturation_type not in ['PV', 'OP']:
            raise ValueError("saturation_type must be either 'PV' or 'OP'")
        self.saturation_type = saturation_type

    def calculate(self, data: Dict[str, np.ndarray], config: Dict[str, Any]) -> float:
        high_key = f'{self.saturation_type.lower()}_high_limit'
        low_key = f'{self.saturation_type.lower()}_low_limit'
        
        high_limit = config.get(high_key, 100)
        low_limit = config.get(low_key, 0)
        
        values = np.array(data[self.saturation_type.lower()])
        
        return np.mean((values >= high_limit) | (values <= low_limit)) * 100

class IntegralAbsoluteError(Metric):
    def calculate(self, data: Dict[str, np.ndarray], config: Dict[str, Any]) -> float:
        error = np.array(data['pv']) - np.array(data['sp'])
        abs_error = np.abs(error)
        time_diff = np.diff(data['timestamp']).astype('timedelta64[s]').astype(float)
        iae = np.sum(abs_error[1:] * time_diff)  # Area under the curve
        pv_range = config.get('pv_range', np.ptp(data['pv']))  # Use config if provided, else calculate
        time_span = (data['timestamp'][-1] - data['timestamp'][0]).total_seconds() # Total time span
        return (iae / pv_range) / time_span  # Normalized IAE 

class ErrorStandardDeviation(Metric):
    def calculate(self, data: Dict[str, np.ndarray], config: Dict[str, Any]) -> float:
        error = np.array(data['pv']) - np.array(data['sp'])
        return np.std(error)

class ErrorMaximum(Metric):
    def calculate(self, data: Dict[str, np.ndarray], config: Dict[str, Any]) -> float:
        error = np.array(data['pv']) - np.array(data['sp'])
        return np.max(np.abs(error))

class SetpointCrossings(Metric):
    def calculate(self, data: Dict[str, np.ndarray], config: Dict[str, Any]) -> float:
        crossings = np.diff(np.sign(np.array(data['pv']) - np.array(data['sp']))) != 0
        time_span = (data['timestamp'][-1] - data['timestamp'][0]).total_seconds() 
        return np.sum(crossings) / time_span  # per day

class ValveTravel(Metric):
    def calculate(self, data: Dict[str, np.ndarray], config: Dict[str, Any]) -> float:
        travel = np.sum(np.abs(np.diff(data['op'])))
        time_span = (data['timestamp'][-1] - data['timestamp'][0]).total_seconds() 
        return travel / time_span  # per day

class ValveReversals(Metric):
    def calculate(self, data: Dict[str, np.ndarray], config: Dict[str, Any]) -> float:
        reversals = np.diff(np.sign(np.diff(data['op']))) != 0
        time_span = (data['timestamp'][-1] - data['timestamp'][0]).total_seconds()
        return np.sum(reversals) / time_span  # per day

class ControlLoop:
    def __init__(self, name: str, data: Dict[str, np.ndarray], config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.data = data
        self.config = config or {}
        self.metrics: Dict[MetricType, Metric] = {}

    def get_metrics(self):
        return self.metrics.items()
    
    def add_metric(self, metric_type: MetricType, metric: Metric):
        self.metrics[metric_type] = metric

    def analyze(self) -> Dict[str, Any]:
        metric_results = {}
        errors = {}
        for metric_type, metric in self.metrics.items():
            try:
                metric_results[metric_type] = metric.calculate(self.data, self.config)
            except Exception as e:
                errors[metric_type]=str(e)
                metric_results[metric_type] = None

        return {
            'metrics': metric_results,
            'errors': errors
        }

class ControlLoopMonitor:
    def __init__(self):
        self.control_loops: List[ControlLoop] = []

    def add_control_loop(self, control_loop: ControlLoop):
        self.control_loops.append(control_loop)

    def analyze_all(self) -> Dict[str, Dict[str, Any]]:
        return {loop.name: loop.analyze() for loop in self.control_loops}



class MetricFactory:
    @staticmethod
    def create(metric_type: MetricType) -> Metric:
        metric_map = {
            MetricType.SERVICE_FACTOR: ServiceFactor(),
            MetricType.OP_SATURATION: Saturation('OP'),
            MetricType.PV_SATURATION: Saturation('PV'),
            MetricType.INTEGRAL_ABSOLUTE_ERROR: IntegralAbsoluteError(),
            MetricType.ERROR_STANDARD_DEVIATION: ErrorStandardDeviation(),
            MetricType.ERROR_MAXIMUM: ErrorMaximum(),
            MetricType.SETPOINT_CROSSINGS: SetpointCrossings(),
            MetricType.VALVE_TRAVEL: ValveTravel(),
            MetricType.VALVE_REVERSALS: ValveReversals(),
        }
        return metric_map.get(metric_type)

