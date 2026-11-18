from industrial_pump_monitoring.simulation.calculations import calculate_next_value
import pytest

def test_correct_calculation():
    current_value = 50
    target_value = 60
    k = 0.1
    noise = 0.2
    next_value = calculate_next_value(current_value, target_value, k, noise)

    assert next_value == pytest.approx(51.2)

def test_cooling():
    current_value = 80
    target_value = 60
    k = 0.1
    noise = 0
    next_value = calculate_next_value(current_value, target_value, k, noise)

    assert next_value == pytest.approx(78)

def test_balanced_value():
    current_value = 60
    target_value = 60
    k = 0.1
    noise = 0.2
    next_value = calculate_next_value(current_value, target_value, k, noise)

    assert next_value == pytest.approx(60.2)

def test_negative_noise():
    current_value = 50
    target_value = 60
    k = 0.1
    noise = -0.5
    next_value = calculate_next_value(current_value, target_value, k, noise)

    assert next_value == pytest.approx(50.5)