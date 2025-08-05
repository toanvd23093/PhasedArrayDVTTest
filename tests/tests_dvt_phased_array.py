import pytest
import numpy as np

# Verify main lobe peak gain
def test_main_lobe_gain(run_S21_scan):
    # Pr = Pt + Gt - Lt - Lfs - Lm + Gr - Lr
    theta, phi, S21_data, Pt, Lt, Lfs, Lm, Lr, Gr, dut_main_lobe_gain, dut_beamwidth, dut_steering_angle_accuracy, dut_sidelobe_level_db = run_S21_scan
    peak_Pr = np.max(np.abs(S21_data))
    peak_gain = peak_Pr-Pt+Lt+Lfs+Lm-Gr+Lr
    diff = np.abs(np.min(peak_gain-dut_main_lobe_gain))
    
    assert peak_gain >= dut_main_lobe_gain, f"Main lobe gain too low: {peak_gain:.2f} dB"

# Verify beamwidth
def test_beamwidth(run_S21_scan):
    theta, phi, S21_data, Pt, Lt, Lfs, Lm, Lr, Gr, dut_main_lobe_gain, dut_beamwidth, dut_steering_angle_accuracy, dut_sidelobe_level_db = run_S21_scan
    num_freq, len_theta, len_phi = S21_data.shape
    center_freq_idx = num_freq // 2  # Choose center frequency
    phi_fixed_idx = 0                # Fix phi=0°

    # Extract 1D pattern in theta direction (E-plane cut)
    pattern_cut = np.abs(S21_data[center_freq_idx, :, phi_fixed_idx])
    pattern_cut_normalized = pattern_cut - np.max(pattern_cut)  # normalize to 0 dB

    # Find -3 dB points
    half_power_idx = np.where(pattern_cut_normalized >= -3)[0]

    # Get HPBW in degrees
    theta_hpbw = theta[half_power_idx]
    HPBW_theta = theta_hpbw[-1] - theta_hpbw[0]

    diff = np.abs(np.min(HPBW_theta-dut_beamwidth))
    
    assert HPBW_theta <= dut_beamwidth, f"Beamwidth too wide: {HPBW_theta:.2f}°"

# Verify steering accuracy
def test_steering_accuracy(run_S21_scan):
    theta, phi, S21_data, Pt, Lt, Lfs, Lm, Lr, Gr, dut_main_lobe_gain, dut_beamwidth, dut_steering_angle_accuracy, dut_sidelobe_level_db = run_S21_scan
    target_angle = 30 

    num_freq, len_theta, len_phi = S21_data.shape
    center_freq_idx = num_freq // 2  # Choose center frequency
    phi_fixed_idx = 0                # Fix phi=0°

    # Extract 1D pattern in theta direction (E-plane cut)
    pattern_cut = np.abs(S21_data[center_freq_idx, :, phi_fixed_idx])

    measured_peak_angle = theta[np.argmax(pattern_cut)]
    error = np.abs(measured_peak_angle - target_angle)

    assert error <= dut_steering_angle_accuracy, f"Steering error too large: {error:.2f}°"

# Verify SLL
def test_sidelobe_level(run_S21_scan):
    theta, phi, S21_data, Pt, Lt, Lfs, Lm, Lr, Gr, dut_main_lobe_gain, dut_beamwidth, dut_steering_angle_accuracy, dut_sidelobe_level_db = run_S21_scan

    num_freq, len_theta, len_phi = S21_data.shape
    center_freq_idx = num_freq // 2  # Choose center frequency
    phi_fixed_idx = 0                # Fix phi=0°

    # Extract 1D pattern in theta direction (E-plane cut)
    pattern_cut = np.abs(S21_data[center_freq_idx, :, phi_fixed_idx])
    
    main_idx = np.argmax(pattern_cut)
    mask = np.ones_like(pattern_cut, dtype=bool)
    mask[max(0, main_idx - 5):min(len(pattern_cut), main_idx + 5)] = False
    sidelobes = pattern_cut[mask]
    max_sll = np.max(sidelobes)
    assert max_sll <= dut_sidelobe_level_db, f"Sidelobe too high: {max_sll:.2f} dB"