from xmci.xmci import ControlLoop, ControlLoopMonitor, MetricFactory, MetricType
import numpy as np


if __name__ == "__main__":
    # Create a control loop
    data = {
        'timestamp': np.array([0, 1, 2, 3, 4]),
        'op': np.array([0, 10, 20, 30, 40])
    }
    config = {
        'op_high_limit': 25,
        'op_low_limit': 5
    }
    control_loop = ControlLoop('my_control_loop', data, config)
    
    # Add a metric to the control loop
    metric = MetricFactory.create(MetricType.OP_SATURATION)
    control_loop.add_metric(MetricType.OP_SATURATION, metric)
    
    # Create a control loop monitor
    monitor = ControlLoopMonitor()
    monitor.add_control_loop(control_loop)
    
    # Analyze all control loops
    results = monitor.analyze_all()
    print(results)