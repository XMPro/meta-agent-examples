# XMPro Objective Functions (XMOF)

A dynamic calculator for industrial metrics that processes real-time data using mathematical expressions. Perfect for digital twins, process monitoring, and performance analysis.

## Key Features
- Calculate complex metrics from streaming data
- Update formulas without interrupting data flow
- Automatic dependency resolution
- Smart caching for performance
- Configurable precision per metric

## Simple Example: OEE Calculation

### Input Values (Raw Data)
```json
{
    "planned_runtime": 480,
    "actual_runtime": 432,
    "ideal_cycle_time": 2.0,
    "total_parts": 198,
    "good_parts": 189
}
```

### Calculations (What We Want to Know)
```json
{
    "availability": {
        "name": "Equipment Availability",
        "description": "Ratio of actual runtime to planned runtime",
        "expression": "actual_runtime/planned_runtime * 100",
        "units": "%",
        "rounding": 1
    },
    "performance": {
        "name": "Performance Efficiency",
        "description": "Actual vs Ideal Production Rate",
        "expression": "total_parts * ideal_cycle_time/actual_runtime * 100",
        "units": "%",
        "rounding": 1
    },
    "quality": {
        "name": "Quality Rate",
        "description": "Good parts vs Total parts",
        "expression": "good_parts/total_parts * 100",
        "units": "%",
        "rounding": 1
    },
    "oee": {
        "name": "Overall Equipment Effectiveness",
        "description": "Combined equipment effectiveness",
        "expression": "availability * performance * quality/10000",
        "units": "%",
        "rounding": 1
    }
}
```

### Output (Results)
```json
[
    {
        "Name": "Equipment Availability",
        "Value": 90.0,
        "Units": "%",
        "Description": "Ratio of actual runtime to planned runtime",
        "Expression": "actual_runtime/planned_runtime * 100",
        "ProcessedTime": "2025-01-09T04:54:19.578515"
    },
    {
        "Name": "Performance Efficiency",
        "Value": 91.7,
        "Units": "%",
        "Description": "Actual vs Ideal Production Rate",
        "Expression": "total_parts * ideal_cycle_time/actual_runtime * 100",
        "ProcessedTime": "2025-01-09T04:54:19.578515"
    },
    {
        "Name": "Quality Rate",
        "Value": 95.5,
        "Units": "%",
        "Description": "Good parts vs Total parts",
        "Expression": "good_parts/total_parts * 100",
        "ProcessedTime": "2025-01-09T04:54:19.578515"
    },
    {
        "Name": "OEE",
        "Value": 78.8,
        "Units": "%",
        "Description": "Combined equipment effectiveness",
        "Expression": "availability * performance * quality/10000",
        "ProcessedTime": "2025-01-09T04:54:19.578515"
    }
]
```

## Smart Features

### Dependency Management
- Automatically determines calculation order
- OEE needs availability, performance, and quality first
- Prevents circular dependencies
- Updates only affected calculations

### Precision Control
```json
{
    "metric_name": {
        "expression": "complex_formula",
        "rounding": 2  // Round to 2 decimal places
    }
}
```
- Set rounding per metric
- Default rounding for all metrics
- Preserves precision in chains of calculations

### Performance Caching
- Caches calculation pathways
- TTL: 1 hour default
- Cache size: 100 entries
- Auto-invalidates on formula changes

## Installation
```bash
pip install xmof==0.0.14
```

## Use Cases
- Manufacturing KPIs
- Process Efficiency
- Energy Analysis
- Equipment Health
- Quality Metrics
- Cost Analysis
- Environmental Monitoring

Built by XMPro for industrial data streams and digital twins.

## License
MIT