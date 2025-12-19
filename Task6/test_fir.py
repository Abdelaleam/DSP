import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from FIR import FIR
from Task4.convolution import Convolution

def parse_specs(filepath):
    specs = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=')
                key = key.strip()
                value = value.strip()
                specs[key] = value
    return specs

def parse_signal(filepath):
    indices = []
    values = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines[3:]:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) >= 2:
                    indices.append(int(parts[0]))
                    values.append(float(parts[1]))
    return np.array(indices), np.array(values)

def parse_expected_coeffs(filepath):
    coeffs = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines[3:]:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) >= 2:
                    coeffs.append(float(parts[1]))
    return np.array(coeffs)

def test_case_1():
    specs = parse_specs('test_cases/Testcase 1/Filter Specifications.txt')    
    filter_type = specs.get('FilterType', '').lower()
    Fs = float(specs.get('FS', 0))
    Fc = float(specs.get('FC', 0))
    transition_band = float(specs.get('TransitionBand', 0))
    stop_attenuation = float(specs.get('StopBandAttenuation', 0))
    
    print(f"\n=== Test Case 1: Filter Coefficients ===")
    print(f"Filter Type: {filter_type}")
    print(f"Fs={Fs}, Fc={Fc}, TransitionBand={transition_band}, StopAttenuation={stop_attenuation}")
    
    if 'low' in filter_type:
        h = FIR.fir_lpf(Fs, Fc, transition_band, stop_attenuation)
    elif 'high' in filter_type:
        h = FIR.fir_hpf(Fs, Fc, transition_band, stop_attenuation)
    else:
        print(f"Unknown filter type: {filter_type}")
        return
    expected = parse_expected_coeffs('test_cases/Testcase 1/LPFCoeff.txt')
    
    if len(h) != len(expected):
        print(f"LENGTH MISMATCH: computed={len(h)}, expected={len(expected)}")
    else:
        print(f"Length matches: {len(h)}")
    
    min_len = min(len(h), len(expected))
    h_trimmed = h[:min_len]
    expected_trimmed = expected[:min_len]
    
    max_error = np.max(np.abs(h_trimmed - expected_trimmed))
    print(f"Max absolute error: {max_error:.10f}")

def test_case_2():
    print(f"\n=== Test Case 2: Signal Filtering ===")
    
    specs = parse_specs('test_cases/Testcase 2/Filter Specifications.txt')
    filter_type = specs.get('FilterType', '').lower()
    Fs = float(specs.get('FS', 0))
    Fc = float(specs.get('FC', 0))
    transition_band = float(specs.get('TransitionBand', 0))
    stop_attenuation = float(specs.get('StopBandAttenuation', 0))
    
    print(f"Filter Type: {filter_type}")
    print(f"Fs={Fs}, Fc={Fc}, TransitionBand={transition_band}, StopAttenuation={stop_attenuation}")
    
    if 'low' in filter_type:
        h = FIR.fir_lpf(Fs, Fc, transition_band, stop_attenuation)
    elif 'high' in filter_type:
        h = FIR.fir_hpf(Fs, Fc, transition_band, stop_attenuation)
    else:
        print(f"Unknown filter type: {filter_type}")
        return
    
    print(f"Filter length: {len(h)}")
    
    x_indices, x_values = parse_signal('test_cases/Testcase 2/ecg400.txt')
    print(f"Input signal length: {len(x_values)}")
    
    signal_x = np.column_stack((x_indices, x_values))
    
    M = (len(h) - 1) // 2
    h_indices = np.arange(-M, M + 1)
    signal_h = np.column_stack((h_indices, h))
    
    result = Convolution.convolve(signal_x, signal_h)
    
    y_indices = result.signal[:, 0].astype(int)
    y_values = result.signal[:, 1]
    
    print(f"Output signal length: {len(y_values)}")
    
    expected_indices, expected_values = parse_signal('test_cases/Testcase 2/ecg_low_pass_filtered.txt')
    print(f"Expected signal length: {len(expected_values)}")
    
    if len(y_values) != len(expected_values):
        print(f"LENGTH MISMATCH: computed={len(y_values)}, expected={len(expected_values)}")
    else:
        print(f"Length matches: {len(y_values)}")
    
    errors = []
    for i, idx in enumerate(expected_indices):
        match_idx = np.where(y_indices == idx)[0]
        if len(match_idx) > 0:
            computed = y_values[match_idx[0]]
            expected = expected_values[i]
            errors.append(abs(computed - expected))
    
    if errors:
        max_error = max(errors)
        print(f"Max absolute error: {max_error:.6f}")
        if max_error < 1.0:
            print("TEST PASSED!")
        else:
            print("TEST FAILED - errors too large")
    else:
        print("No matching indices found!")

def test_case_3():
    specs = parse_specs('test_cases/Testcase 3/Filter Specifications.txt')    
    filter_type = specs.get('FilterType', '').lower()
    Fs = float(specs.get('FS', 0))
    Fc = float(specs.get('FC', 0))
    transition_band = float(specs.get('TransitionBand', 0))
    stop_attenuation = float(specs.get('StopBandAttenuation', 0))
    
    print(f"\n=== Test Case 3: HPF Coefficients (Blackman Window) ===")
    print(f"Filter Type: {filter_type}")
    print(f"Fs={Fs}, Fc={Fc}, TransitionBand={transition_band}, StopAttenuation={stop_attenuation}")
    
    if 'low' in filter_type:
        h = FIR.fir_lpf(Fs, Fc, transition_band, stop_attenuation)
    elif 'high' in filter_type:
        h = FIR.fir_hpf(Fs, Fc, transition_band, stop_attenuation)
    else:
        print(f"Unknown filter type: {filter_type}")
        return
    
    print(f"Filter length: {len(h)}")
    expected = parse_expected_coeffs('test_cases/Testcase 3/HPFCoefficients.txt')
    print(f"Expected length: {len(expected)}")
    
    if len(h) != len(expected):
        print(f"LENGTH MISMATCH: computed={len(h)}, expected={len(expected)}")
    else:
        print(f"Length matches: {len(h)}")
    
    min_len = min(len(h), len(expected))
    h_trimmed = h[:min_len]
    expected_trimmed = expected[:min_len]
    
    max_error = np.max(np.abs(h_trimmed - expected_trimmed))
    print(f"Max absolute error: {max_error:.10f}")
    
    if max_error < 0.001:
        print("TEST PASSED!")
    else:
        print("TEST FAILED")

def test_case_4():
    print(f"\n=== Test Case 4: HPF Signal Filtering (Blackman Window) ===")
    
    specs = parse_specs('test_cases/Testcase 4/Filter Specifications.txt')
    filter_type = specs.get('FilterType', '').lower()
    Fs = float(specs.get('FS', 0))
    Fc = float(specs.get('FC', 0))
    transition_band = float(specs.get('TransitionBand', 0))
    stop_attenuation = float(specs.get('StopBandAttenuation', 0))
    
    print(f"Filter Type: {filter_type}")
    print(f"Fs={Fs}, Fc={Fc}, TransitionBand={transition_band}, StopAttenuation={stop_attenuation}")
    
    if 'low' in filter_type:
        h = FIR.fir_lpf(Fs, Fc, transition_band, stop_attenuation)
    elif 'high' in filter_type:
        h = FIR.fir_hpf(Fs, Fc, transition_band, stop_attenuation)
    else:
        print(f"Unknown filter type: {filter_type}")
        return
    
    print(f"Filter length: {len(h)}")
    
    x_indices, x_values = parse_signal('test_cases/Testcase 4/ecg400.txt')
    print(f"Input signal length: {len(x_values)}")
    
    signal_x = np.column_stack((x_indices, x_values))
    
    M = (len(h) - 1) // 2
    h_indices = np.arange(-M, M + 1)
    signal_h = np.column_stack((h_indices, h))
    
    result = Convolution.convolve(signal_x, signal_h)
    
    y_indices = result.signal[:, 0].astype(int)
    y_values = result.signal[:, 1]
    
    print(f"Output signal length: {len(y_values)}")
    
    expected_indices, expected_values = parse_signal('test_cases/Testcase 4/ecg_high_pass_filtered.txt')
    print(f"Expected signal length: {len(expected_values)}")
    
    if len(y_values) != len(expected_values):
        print(f"LENGTH MISMATCH: computed={len(y_values)}, expected={len(expected_values)}")
    else:
        print(f"Length matches: {len(y_values)}")
    
    errors = []
    for i, idx in enumerate(expected_indices):
        match_idx = np.where(y_indices == idx)[0]
        if len(match_idx) > 0:
            computed = y_values[match_idx[0]]
            expected = expected_values[i]
            errors.append(abs(computed - expected))
    
    if errors:
        max_error = max(errors)
        print(f"Max absolute error: {max_error:.6f}")
        if max_error < 1.0:
            print("TEST PASSED!")
        else:
            print("TEST FAILED - errors too large")
    else:
        print("No matching indices found!")

def main():
    test_case_4()

if __name__ == '__main__':
    main()
