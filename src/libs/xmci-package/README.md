# XMPro Control Insights

XMPro Control Insights is a Python library for monitoring and analyzing the performance of industrial control loops using key performance indicators (KPIs). This package offers a flexible framework to measure metrics and detect control system issues such as saturation, tuning problems, and disturbances.

## Features

- **Built-in Metrics**: Includes metrics such as Service Factor, OP Saturation, PV Saturation, Integral Absolute Error, and more.
- **Custom Metrics**: Allows for the creation of custom metrics by extending the `Metric` abstract base class.
- **Configurable Analysis**: Supports custom configuration for different control loop settings.
- **Control Loop Management**: Use `ControlLoop` and `ControlLoopMonitor` classes to manage and analyze multiple control loops.
- **Factory Pattern**: Easily create metrics using the `MetricFactory`.

## Installation

Install the package via pip:

```bash
pip install xmci
```

## Usage

Create a control loop, add metrics, and analyze the data:

```python
from xmci import ControlLoop, MetricFactory, MetricType
from datetime import datetime, timedelta

data = {
    'mode': [1, 1, 0, 1],
    'op': [10, 50, 90, 100],
    'pv': [25, 30, 40, 45],
    'sp': [30, 35, 40, 50],
    'timestamp': [datetime.now(), datetime.now() + timedelta(minutes=1), ...]
}

config = {'op_high_limit': 100, 'pv_high_limit': 80}

# Create a control loop and add a metric
loop = ControlLoop('Compressor Loop', data, config)
loop.add_metric(MetricType.OP_SATURATION, MetricFactory.create(MetricType.OP_SATURATION))

# Analyze the control loop
results = loop.analyze()
print(results)
```

Monitor multiple control loops:

```python
from xmci import ControlLoopMonitor

monitor = ControlLoopMonitor()
monitor.add_control_loop(loop)
all_results = monitor.analyze_all()
print(all_results)
```

## Dependencies

- `numpy`: For numerical computations.
- `datetime`: To handle timestamps.

## License

This package is licensed under the MIT License.
