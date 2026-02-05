
def calculate_cost(response, settings):
    """
    Calcula el costo de una llamada a la API
    """
    usage = response.usage
    
    input_cost = (usage.prompt_tokens / 1_000_000) * settings.price_input
    output_cost = (usage.completion_tokens / 1_000_000) * settings.price_output
    total_cost = input_cost + output_cost
    
    return {
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(total_cost, 6)
    }