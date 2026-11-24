from industrial_pump_monitoring.simulation.runner import run_simulation_cycle, run_simulation
from industrial_pump_monitoring.simulation.pump import IndustrialPump
import pytest

def test_run_simulation_cycle(monkeypatch):
    pump_01 = IndustrialPump("PUMP-01", "NORMAL", 50.0, 2.0, 3.0)
    pump_02 = IndustrialPump("PUMP-02", "OFF", 50.0, 0.5, 2.0)
    pump_03 = IndustrialPump("PUMP-03", "ABNORMAL", 70.0, 2.0, 3.0)

    pumps = [pump_01, pump_02, pump_03]
    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )
    measurements = run_simulation_cycle(pumps)

    assert measurements == [
        {
            "pump_id": "PUMP-01",
            "temperature": pytest.approx(51.0),
            "vibration": pytest.approx(1.84),
            "pressure": pytest.approx(3.30)
        },
        {
            "pump_id": "PUMP-02",
            "temperature": pytest.approx(48.0),
            "vibration": pytest.approx(0.42),
            "pressure": pytest.approx(1.55)
        },
        {
            "pump_id": "PUMP-03",
            "temperature": pytest.approx(71.50),
            "vibration": pytest.approx(2.60),
            "pressure": pytest.approx(2.70)
        }
    ]

def test_run_simulation_cycle_empty_list():
    assert run_simulation_cycle([]) == []

def test_run_simulation_three_cycles(monkeypatch):

    pump = IndustrialPump("PUMP-01", "NORMAL", 50.0, 2.0, 3.0)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    sleep_calls = []

    def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.runner.time.sleep",
        fake_sleep
    )

    measurements = run_simulation(
        [pump],
        cycles=3,
        interval=5
    )

    assert len(measurements) == 3
    assert sleep_calls == [5, 5]
    assert measurements[0][0]["temperature"] == pytest.approx(51.0)
    assert measurements[1][0]["temperature"] == pytest.approx(51.9)
    assert measurements[2][0]["temperature"] == pytest.approx(52.71)

def test_run_simulation_zero_cycles(monkeypatch):

    pump = IndustrialPump("PUMP-01", "NORMAL", 50.0, 2.0, 3.0)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    sleep_calls = []

    def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.runner.time.sleep",
        fake_sleep
    )

    measurements = run_simulation(
        [pump],
        cycles=0,
        interval=5
    )

    assert measurements == []
    assert sleep_calls == []

def test_run_simulation_one_cycle(monkeypatch):

    pump = IndustrialPump("PUMP-01", "NORMAL", 50.0, 2.0, 3.0)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.pump.random.uniform",
        lambda a, b: 0.0
    )

    sleep_calls = []

    def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(
        "industrial_pump_monitoring.simulation.runner.time.sleep",
        fake_sleep
    )

    measurements = run_simulation(
        [pump],
        cycles=1,
        interval=5
    )

    assert sleep_calls == []
    assert measurements[0][0]["temperature"] == pytest.approx(51.0)
    assert measurements[0][0]["vibration"] == pytest.approx(1.84)
    assert measurements[0][0]["pressure"] == pytest.approx(3.30)