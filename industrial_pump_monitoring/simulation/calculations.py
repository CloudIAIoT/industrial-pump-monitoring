def calculate_next_value(current_value, target_value, k, noise):
    return current_value + k * (target_value - current_value) + noise