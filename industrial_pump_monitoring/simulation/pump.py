from industrial_pump_monitoring.simulation.calculations import calculate_next_value
import random
import time

VALID_STATUSES = {"NORMAL", "OFF", "ABNORMAL"}

TEMPERATURE_TARGETS = {
    "OFF": 30.0,
    "NORMAL": 60.0,
    "ABNORMAL": 85.0

}

VIBRATION_TARGETS = {
    "OFF": 0.1,
    "NORMAL": 1.2,
    "ABNORMAL": 5.0
}

PRESSURE_TARGETS = {
    "OFF": 0.5,
    "NORMAL": 4.0,
    "ABNORMAL": 2.0
}

class IndustrialPump:
    def __init__(self, pump_id, status, temperature, vibration, pressure):
        self.pump_id = pump_id
        self.status = status
        self.temperature = temperature
        self.vibration = vibration
        self.pressure = pressure

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        if new_status not in VALID_STATUSES:
            raise ValueError("Invalid status")
        
        self._status = new_status

    def update_temperature(self, k=0.1):
        target_temperature = TEMPERATURE_TARGETS[self.status]
        self.temperature = calculate_next_value(
            self.temperature,
            target_temperature,
            k,
            random.uniform(-0.2, 0.2)
        )

    def update_vibration(self, k=0.2):
        target_vibration = VIBRATION_TARGETS[self.status]
        new_vibration = calculate_next_value(
            self.vibration, 
            target_vibration,
            k,
            random.uniform(-0.05, 0.05)
        )
        self.vibration = max(0, new_vibration)

    def update_pressure(self, k=0.3):
        target_pressure = PRESSURE_TARGETS[self.status]
        new_pressure = calculate_next_value(
            self.pressure, 
            target_pressure,
            k,
            random.uniform(-0.05, 0.05)
        )
        self.pressure = max(0, new_pressure)

    def update_measurements(self):
        self.update_temperature()
        self.update_vibration()
        self.update_pressure()
    
    def read_measurements(self):
        return {
            "pump_id": self.pump_id,
            "temperature": self.temperature,
            "vibration": self.vibration,
            "pressure": self.pressure
        }

pump_01 = IndustrialPump("PUMP-01", "NORMAL", 55.5, 1.4, 3.8)
print(pump_01.read_measurements())
    

