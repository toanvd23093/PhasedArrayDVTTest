import json
import os

class DUTConfig:
    def __init__(self, json_filename='dut_config.json'):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'tests', json_filename)
        
        with open(config_path, 'r') as f:
            self.specs = json.load(f)
        
        self.Name             = self.specs['name']
        self.Version          = self.specs['version']
        self.CenterFreq       = self.specs['center_freq']
        self.NumElements      = self.specs['num_elements']
        self.Beamwidth        = self.specs['beamwidth_deg']
        self.SteeringAccuracy = self.specs['steering_accuracy_deg']
        self.MainlobeGain_dB  = self.specs['main_lobe_gain_dB']
        self.SidelobeLevel_dB = self.specs['sidelobe_level_dB']
        self.S11_Max_dB       = self.specs['s11_max_dB']

    def methods(self):
        return list(self.specs.keys())
