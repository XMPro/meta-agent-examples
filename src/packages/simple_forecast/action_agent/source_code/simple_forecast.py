import time

seconds_to_wait = None
temperature_history = []
max_history_length = 5 

def on_create(data: dict) -> dict | None:
    global seconds_to_wait
    seconds_to_wait = data.get("seconds_to_wait", 0)

    return {}


def on_receive(data: dict) -> dict | None:
    
    start_time = time.time()

    temperature = data.get("temperature", 0)
    
    wait_time = int(float(seconds_to_wait))
    time.sleep(wait_time)
    
    forecasted_temperature = _calculate_forecast(temperature)

    elapsed_seconds =  f"{(time.time() - start_time):.6f}"

    result = {
        "forecasted_temperature": forecasted_temperature,
        "elapsed_seconds": elapsed_seconds
    }
    
    return result

def _calculate_forecast(temperature: float) -> float:
    global temperature_history

    # Add the new temperature to the history
    temperature_history.append(temperature)
    
    # Keep only the most recent temperatures
    if len(temperature_history) > max_history_length:
        temperature_history = temperature_history[-max_history_length:]
    
    # Forecast the next temperature (simple moving average)
    return sum(temperature_history) / len(temperature_history)
