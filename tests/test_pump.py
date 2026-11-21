from industrial_pump_monitoring.simulation.pump import IndustrialPump
import pytest

def test_create_valid_pump():
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 54, 1.2, 3.8)
    assert pump_01.pump_id == "PUMP-01"
    assert pump_01.status == "NORMAL"
    assert pump_01.temperature == 54
    assert pump_01.vibration == 1.2
    assert pump_01.pressure == 3.8

def test_create_invalid_status():

    with pytest.raises(ValueError):
        pump_01 = IndustrialPump("PUMP-01", "ACTIVE", 54, 1.2, 3.8)

def test_change_valid_status():
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 54, 1.2, 3.8)
    pump_01.status = "OFF"

    assert pump_01.status == "OFF"

def test_change_invalid_status():
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 54, 1.2, 3.8)

    with pytest.raises(ValueError):
        pump_01.status = "INACTIVE"
    
    assert pump_01.status == "NORMAL"
    
def test_update_temperature_normal(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 50, 1.2, 3.8)
    
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.1
    )

    pump_01.update_temperature()

    assert pump_01.temperature == pytest.approx(51.1)

def test_update_temperature_off(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "OFF", 50, 0.5, 4.6)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    pump_01.update_temperature()

    assert pump_01.temperature == pytest.approx(48)

def test_update_vibration_normal(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 50, 2.0, 3.8)
    
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    pump_01.update_vibration()

    assert pump_01.vibration == pytest.approx(1.84)

def test_update_vibration_abnormal(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "ABNORMAL", 69, 2.0, 1.8)
    
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    pump_01.update_vibration()

    assert pump_01.vibration == pytest.approx(2.60)


def test_update_pressure_normal(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 50, 2.0, 3.0)
    
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    pump_01.update_pressure()

    assert pump_01.pressure == pytest.approx(3.30)

def test_update_pressure_off(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "OFF", 50, 0.5, 2.0)
    
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    pump_01.update_pressure()

    assert pump_01.pressure == pytest.approx(1.55)

def test_update_vibration_normal(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 50, 2.0, 3.8)
    
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    pump_01.update_vibration()

    assert pump_01.vibration == pytest.approx(1.84)

def test_update_vibration_abnormal(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "ABNORMAL", 69, 2.0, 1.8)
    
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    pump_01.update_vibration()

    assert pump_01.vibration == pytest.approx(2.60)


def test_update_pressure_normal(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 50, 2.0, 3.0)
    
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    pump_01.update_pressure()

    assert pump_01.pressure == pytest.approx(3.30)

def test_update_measurements(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "OFF", 50, 0.5, 2.0)
    pump_02 = IndustrialPump("PUMP-02", "ABNORMAL", 70, 2.0, 3.0)

    
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    pump_01.update_measurements()
    pump_02.update_measurements()

    assert pump_01.pressure == pytest.approx(1.55)
    assert pump_01.vibration == pytest.approx(0.42)
    assert pump_01.temperature == pytest.approx(48.0)
    assert pump_02.pressure == pytest.approx(2.70)
    assert pump_02.vibration == pytest.approx(2.60)
    assert pump_02.temperature == pytest.approx(71.50)

def test_vibration_lower_bound(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "OFF", 50, 0.0, 2.0)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: -0.05
    )

    pump_01.update_measurements()

    assert pump_01.vibration == 0

def test_pressure_minimum_conditions(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "OFF", 50, 0.3, 0.0)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: -0.05
    )

    pump_01.update_pressure()

    assert pump_01.pressure == pytest.approx(0.10)

def test_read_measurements():
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 55.5, 1.4, 3.8)

    measurements = pump_01.read_measurements()

    assert measurements == {
        "pump_id": "PUMP-01",
        "temperature": 55.5,
        "vibration": 1.4,
        "pressure": 3.8
    }

def test_read_measurements_after_update(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 50.0, 2.0, 3.0)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )
    pump_01.update_measurements()
    measurements = pump_01.read_measurements()

    assert measurements == {
        "pump_id": "PUMP-01",
        "temperature": pytest.approx(51.0),
        "vibration": pytest.approx(1.84),
        "pressure": pytest.approx(3.30)
    }