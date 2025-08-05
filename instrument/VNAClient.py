import pyvisa
import numpy as np
import time

class VNAClient:
    def __init__(self, ip_address: str, timeout_ms: int = 70000):
        self.rm = pyvisa.ResourceManager()
        self.vna = self.rm.open_resource(ip_address)
        self.vna.timeout = timeout_ms
        self.vna.clear()

    def configure(self, calset_name, n_points=201, start_freq=8e9, stop_freq=12e9, power_dBm=15):
        self.vna.write(f'SENS:CORR:CSET:ACT "{calset_name}",0')
        self.vna.write('CALC:FORM MLOG')
        self.vna.write(f'SENS:SWE:POIN {n_points}')
        self.vna.write(f'SENS:FREQ:STAR {start_freq}')
        self.vna.write(f'SENS:FREQ:STOP {stop_freq}')
        self.vna.write(f'SOUR:POW1 {power_dBm}')

    def get_frequencies(self) -> np.ndarray:
        freqs = self.vna.query_ascii_values('SENS:FREQ:DATA?')
        return np.array(freqs)

    def _get_complex_data(self, trace_name: str) -> np.ndarray:
        self.vna.write(f'CALC:PAR:SEL "{trace_name}"')
        self.vna.write('CALC:FORM POL')
        self.vna.write('CALC:DATA? SDATA')
        raw_data = self.vna.read_raw()
        data = np.frombuffer(raw_data, dtype='>f8')
        return data[::2] + 1j * data[1::2]

    def get_s11_data(self):
        self.sweep()
        s11 = self._get_complex_data("CH1_S11_1")
        return s11

    def get_s21_data(self):
        self.sweep()
        s21 = self._get_complex_data("CH1_S21_1")
        return s21

    def close(self):
        self.vna.write('*CLS')
        self.vna.close()
        self.rm.close()