import json
from datetime import datetime
from xmof import IndustrialCalculator  # version=0.0.14 package=xmof

# Global calculator instance
calculator = None

def on_create(data: dict) -> dict | None:
    """Initialize the script with provided data"""
    global calculator
    
    try:
        config = json.loads(data.get("config", "{}"))
        calculator = IndustrialCalculator(
            default_rounding=config.get("default_rounding", None),
            cache_ttl=config.get("cache_ttl", 3600)  # Default 1 hour TTL
        )
        return {"initialized": ""}
    except Exception as e:
        return {"error": str(e)}

def on_receive(data: dict) -> dict:
    """Process received event data"""
    global calculator
    
    try:
        # Extract input values
        input_values = json.loads(data['values'])
        
        # Get calculations configuration
        config = {
            "input_values": input_values,
            "calculations": json.loads(data.get("calculations", "{}")),
            "default_rounding": data.get("default_rounding")
        }
        
        # Parse configuration and evaluate
        calculator.parse_config(config)
        result = calculator.evaluate()
        
        # Format results
        formatted_results = []
        processed_time = datetime.now().isoformat()
        
        for calc_name, value in result["results"].items():
            formula = calculator.formulas[calc_name]
            formatted_results.append({
                "Name": formula.name,
                "Value": value,
                "Units": formula.units,
                "Description": formula.description,
                "Expression": formula.expression,
                "ProcessedTime": processed_time
            })
        
        return {
            "results": json.dumps(formatted_results),
            "errors": json.dumps(result["errors"]) if result.get("errors") else None,
            "cache_info": result["cache_info"]
        }
        
    except Exception as e:
        return {"error": str(e)}

def on_destroy() -> dict | None:
    """Clean up resources"""
    global calculator
    calculator = None
    return {"destroyed": ""}

