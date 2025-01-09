
# XMOF - Industrial Formula Calculator

A powerful Python library for managing and evaluating complex industrial calculations with automatic dependency resolution and caching.

## Features

- 🔄 Automatic dependency resolution for complex formula chains
- 🚀 Efficient caching system with time-based expiration
- 📐 Configurable precision control with per-formula rounding
- 🔍 Built-in mathematical constants (π, e)
- 🛡️ Circular dependency detection
- 📊 Rich calculation metadata and error reporting

## Installation

```bash
pip install xmof
```

## Quick Start

```python
from xmof import IndustrialCalculator

# Initialize calculator with default 2 decimal rounding
calculator = IndustrialCalculator(default_rounding=2)

# Define your calculations
config = {
    "input_values": {
        "temperature": 25.0,
        "pressure": 101.325
    },
    "calculations": {
        "vapor_pressure": {
            "name": "Vapor Pressure",
            "description": "Antoine equation for vapor pressure",
            "expression": "10**(7.96681 - 1668.21/(temperature + 228.0))",
            "units": "kPa"
        },
        "relative_humidity": {
            "name": "Relative Humidity",
            "description": "Ratio of vapor pressures",
            "expression": "vapor_pressure/pressure * 100",
            "units": "%"
        }
    }
}

# Parse configuration and evaluate
calculator.parse_config(config)
result = calculator.evaluate()
print(result["results"])
```

## Configuration Format

The calculator accepts a configuration dictionary with the following structure:

```python
{
    "input_values": {
        "variable1": value1,
        "variable2": value2
    },
    "calculations": {
        "calc1": {
            "name": "Display Name",
            "description": "Formula description",
            "expression": "mathematical expression",
            "units": "units of measurement",
            "rounding": 2  # optional, overrides default
        }
    },
    "default_rounding": 2  # optional
}
```

## Features in Detail

### Dependency Management
- Automatically detects dependencies between formulas
- Creates optimal calculation order
- Prevents circular dependencies
- Caches dependency graphs for improved performance

### Formula Support
- Full mathematical expression support via SymPy
- Access to mathematical constants (π, e)
- Support for unit tracking
- Per-formula rounding control

### Error Handling
- Comprehensive error reporting
- Clear circular dependency detection
- Invalid expression handling
- Missing variable detection

## Performance Considerations

The calculator uses caching to optimize performance:
- Dependency graphs are cached with a configurable TTL
- Default cache size: 100 entries
- Default cache TTL: 3600 seconds (1 hour)

## Example Use Cases

```python
# Process engineering calculations
config = {
    "input_values": {
        "flow_rate": 100,
        "density": 1000
    },
    "calculations": {
        "mass_flow": {
            "name": "Mass Flow Rate",
            "description": "Mass flow calculation",
            "expression": "flow_rate * density",
            "units": "kg/h"
        }
    }
}

# Chemical reaction yields
config = {
    "input_values": {
        "initial_concentration": 2.0,
        "time": 3600
    },
    "calculations": {
        "final_concentration": {
            "name": "Final Concentration",
            "description": "First-order reaction kinetics",
            "expression": "initial_concentration * e**(-0.0005 * time)",
            "units": "mol/L"
        }
    }
}
```

## Contributing

Contributions are welcome! Please feel free to contact XMPro.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact XMPro.
