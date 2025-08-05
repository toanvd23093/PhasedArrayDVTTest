import json
import os

class TestConfig:
    def __init__(self, json_filename='test_config.json'):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'tests', json_filename)
        
        with open(config_path, 'r') as f:
            self.specs = json.load(f)

        self.Name              = self.specs['name']
        self.NumSweepPoints    = self.specs['sweep_points']
        self.StartFreq         = self.specs['start_freq_Hz']
        self.StopFreq          = self.specs['stop_freq_Hz']
        self.InputPower        = self.specs['power_dBm']
        self.TX_cable_loss_dB  = self.specs['TX_cable_loss_dB']
        self.RX_cable_loss_dB  = self.specs['RX_cable_loss_dB']
        self.Misc_loss_dB      = self.specs['Misc_loss_dB']
        self.RX_gain_dBi       = self.specs['RX_gain_dBi']
        self.Range             = self.specs['range']
        self.AzimuthRange      = self.specs['azimuth_range']
        self.ElevationRange    = self.specs['elevation_range']
        self.Step              = self.specs['step_deg']
        self.MCU_IP            = self.specs['mcu_ip']
        self.VNA_IP            = self.specs['vna_ip']
        self.CalibrationSet    = self.specs['calc_set']
        self.LogDir            = self.specs['log_dir']

    def methods(self):
        return list(self.specs.keys())
