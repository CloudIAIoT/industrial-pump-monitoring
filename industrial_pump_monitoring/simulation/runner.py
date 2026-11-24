import time
from industrial_pump_monitoring.simulation.pump import IndustrialPump

def run_simulation_cycle(pumps):
    measurements_list = []

    for pump in pumps:
        pump.update_measurements()
        measurements_list.append(pump.read_measurements())

    return measurements_list

def run_simulation(pumps, cycles, interval=5):
    cycle_measurements = []
    for i in range(cycles):
        cycle_measurements.append(run_simulation_cycle(pumps))

        if i < cycles - 1:
            time.sleep(interval)
    return cycle_measurements