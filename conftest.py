import pytest
import numpy as np

from instrument.SphericalScan import SphericalScan  
from instrument.VNAClient import VNAClient
from instrument.MCUClient import MCUClient

from configs.DUTConfig import DUTConfig
from configs.TestConfig import TestConfig

@pytest.fixture(scope="session")
def run_S21_scan():
    # --- Setup ---
    DUT = DUTConfig()
    TestCfg = TestConfig()

    az_range = TestCfg.AzimuthRange
    el_range = TestCfg.ElevationRange
    angle_step = TestCfg.Step

    phi = np.arange(az_range[0], az_range[1], angle_step)
    theta = np.arange(el_range[0], el_range[1], angle_step)

    VNA = VNAClient(ip_address=TestCfg.VNA_IP)
    MCU = MCUClient(ip_address=TestCfg.MCU_IP, 
                    port=213,
                    num_point_fast_arm=len(phi),
                    num_points_slow_arm=len(theta))

    Scanner = SphericalScan(DUT, MCU, VNA, TestCfg)
    S21_data = Scanner.run_scan()

    d = TestCfg.Range
    f_0 = DUT.CenterFreq
    lambda_0 = 3e8 / f_0

    # Free space loss
    Lfs = 20 * np.log10(4 * np.pi * d / lambda_0)
    Pt = TestCfg.InputPower
    Gr = TestCfg.RX_gain_dBi
    Lt = TestCfg.TX_cable_loss_dB
    Lr = TestCfg.RX_cable_loss_dB
    Lm = TestCfg.Misc_loss_dB

    dut_main_lobe_gain = DUT.MainlobeGain_dB
    dut_beamwidth = DUT.Beamwidth
    dut_steering_angle_accuracy = DUT.SteeringAccuracy
    dut_sidelobe_level_db = DUT.SidelobeLevel_dB

    yield (theta, phi, S21_data, Pt, Lt, Lfs, Lm, Lr, Gr,
           dut_main_lobe_gain, dut_beamwidth, 
           dut_steering_angle_accuracy, dut_sidelobe_level_db)

    # --- Teardown ---
    DUT.clear()
    TestCfg.clear()
    VNA.clear()
    MCU.clear()
    Scanner.clear()

def pytest_configure(config):
    config._custom_test_results = {}

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    import json
    
    with open("test_results.json", "w") as f:
        json.dump(session.config._custom_test_results, f, indent=4)