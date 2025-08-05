import numpy as np
import time
import os

class SphericalScan:
    def __init__(self, DUT, MCU, VNA, TestCfg):

        self.scan_status = False

        self.DUT = DUT
        self.VNA = VNA
        self.TestCfg = TestCfg
        self.MCU = MCU
        
        self.VNA.configure(calset_name = self.TestCfg.CalibrationSet, 
            n_points   = self.TestCfg.NumSweepPoints, 
            start_freq = self.TestCfg.StartFreq, 
            stop_freq  = self.TestCfg.StopFreq, 
            power_dBm  = self.TestCfg.InputPower)

        az_range = self.TestCfg.AzimuthRange
        el_range = self.TestCfg.ElevationRange
        angle_step = self.TestCfg.Step

        self.phi = np.arange(az_range[0],az_range[1],angle_step)
        self.theta = np.arange(el_range[0],el_range[1],angle_step)
        self.freq = self.VNA.get_frequencies()

        logName = self.DUT.Name + self.DUT.Version + '.npy'
        self.LogDir = os.path.join(os.path.dirname(__file__), '..', TestCfg.LogDir, logName) 

    def __collect_s21(self):    
        return self.VNA.get_s21_data()

    def run_scan(self, delay_sec=2):

        for i,phi in enumerate(self.phi):
            theta_axis = self.theta if phi % 2 == 0 else reversed(self.theta)

            for j,theta in enumerate(theta_axis):
                self.MCU.move_motors(theta, phi)
                time.sleep(delay_sec)
                s21 = self.__collect_s21()
                self.S21[:, j, i] = s21

        fixed = np.zeros_like(self.S21)
        for i,phi in enumerate(self.phi):
            if i % 2 == 0:
                fixed[:, :, i] = self.S21[:, :, i]
            else:
                fixed[:, :, i] = self.S21[:, ::-1, i]

        self.fixed_data = fixed

        # Store data to log dir
        np.save(self.LogDir, self.fixed_data)

        loaded_array = np.load(self.LogDir)

        if np.array_equal(self.fixed_data, loaded_array):
            self.scan_status = True
        
        return self.fixed_data

    
