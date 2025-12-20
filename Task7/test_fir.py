import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from FIR import FIR
from Task4.convolution import Convolution
from Task5.Fourier import Fourier



def Compare_Signals(file_name,Your_indices,Your_samples):      
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.16:
            continue
        else:
            print("Test case failed, your signal have different values from the expected one") 
            return
    print("Test case passed successfully")


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

def filter_with_dft_idft(x_values, h):

    N = len(x_values) + len(h) - 1
    
    x_padded = np.zeros(N)
    h_padded = np.zeros(N)
    x_padded[:len(x_values)] = x_values
    h_padded[:len(h)] = h
    
    X_amp, X_phase = Fourier.DFT(x_padded)
    H_amp, H_phase = Fourier.DFT(h_padded)
    
    X = [X_amp[k] * np.exp(1j * X_phase[k]) for k in range(N)]
    H = [H_amp[k] * np.exp(1j * H_phase[k]) for k in range(N)]
    
    Y = [X[k] * H[k] for k in range(N)]
    
    Y_amp = [abs(y) for y in Y]
    Y_phase = [np.angle(y) for y in Y]
    
    y_values = Fourier.IDFT(Y_amp, Y_phase)
    
    return np.array(y_values)

def compare_with_expected(y_values, y_indices, expected_values, expected_indices, method_name=""):
    errors = []
    for i, idx in enumerate(expected_indices):
        match_idx = np.where(y_indices == idx)[0]
        if len(match_idx) > 0:
            computed = y_values[match_idx[0]]
            expected = expected_values[i]
            errors.append(abs(computed - expected))
    
    if errors:
        max_error = max(errors)
        print(f"  {method_name} Max absolute error: {max_error:.6f}")
        return max_error
    else:
        print(f"  {method_name} No matching indices found!")
        return float('inf')

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
    M = (len(h) - 1) // 2
    h_indices = list(range(-M, M + 1))
    h_samples = h.tolist()
    Compare_Signals('test_cases/Testcase 1/LPFCoeff.txt', h_indices, h_samples)

def test_case_2():
    print(f"\n=== Test Case 2: LPF Signal Filtering ===")
    
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
    
    expected_indices, expected_values = parse_signal('test_cases/Testcase 2/ecg_low_pass_filtered.txt')
    print(f"Expected signal length: {len(expected_values)}")
    
    # Method 1: Convolution
    print("\n[Method 1: Convolution]")
    signal_x = np.column_stack((x_indices, x_values))
    M = (len(h) - 1) // 2
    h_indices = np.arange(-M, M + 1)
    signal_h = np.column_stack((h_indices, h))
    
    result_conv = Convolution.convolve(signal_x, signal_h)
    y_indices_conv = result_conv.signal[:, 0].astype(int).tolist()
    y_values_conv = result_conv.signal[:, 1].tolist()
    print(f"  Output signal length: {len(y_values_conv)}")
    Compare_Signals('test_cases/Testcase 2/ecg_low_pass_filtered.txt', y_indices_conv, y_values_conv)
    
    # Method 2: DFT/IDFT
    print("\n[Method 2: DFT/IDFT]")
    y_values_dft = filter_with_dft_idft(x_values, h)
    first_idx = int(x_indices[0]) + (-M)
    y_indices_dft = list(range(first_idx, first_idx + len(y_values_dft)))
    y_values_dft_list = y_values_dft.tolist()
    print(f"  Output signal length: {len(y_values_dft_list)}")
    Compare_Signals('test_cases/Testcase 2/ecg_low_pass_filtered.txt', y_indices_dft, y_values_dft_list)

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
    
    # Use Compare_Signals function - indices centered at 0
    M = (len(h) - 1) // 2
    h_indices = list(range(-M, M + 1))
    h_samples = h.tolist()
    Compare_Signals('test_cases/Testcase 3/HPFCoefficients.txt', h_indices, h_samples)

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
    
    expected_indices, expected_values = parse_signal('test_cases/Testcase 4/ecg_high_pass_filtered.txt')
    print(f"Expected signal length: {len(expected_values)}")
    
    # Method 1: Convolution
    print("\n[Method 1: Convolution]")
    signal_x = np.column_stack((x_indices, x_values))
    M = (len(h) - 1) // 2
    h_indices = np.arange(-M, M + 1)
    signal_h = np.column_stack((h_indices, h))
    
    result_conv = Convolution.convolve(signal_x, signal_h)
    y_indices_conv = result_conv.signal[:, 0].astype(int).tolist()
    y_values_conv = result_conv.signal[:, 1].tolist()
    print(f"  Output signal length: {len(y_values_conv)}")
    Compare_Signals('test_cases/Testcase 4/ecg_high_pass_filtered.txt', y_indices_conv, y_values_conv)
    
    # Method 2: DFT/IDFT
    print("\n[Method 2: DFT/IDFT]")
    y_values_dft = filter_with_dft_idft(x_values, h)
    first_idx = int(x_indices[0]) + (-M)
    y_indices_dft = list(range(first_idx, first_idx + len(y_values_dft)))
    y_values_dft_list = y_values_dft.tolist()
    print(f"  Output signal length: {len(y_values_dft_list)}")
    Compare_Signals('test_cases/Testcase 4/ecg_high_pass_filtered.txt', y_indices_dft, y_values_dft_list)

def test_case_5():
    """Test Case 5: Band Pass Filter Coefficients"""
    specs = parse_specs('test_cases/Testcase 5/Filter Specifications.txt')    
    filter_type = specs.get('FilterType', '').lower()
    Fs = float(specs.get('FS', 0))
    F1 = float(specs.get('F1', 0))
    F2 = float(specs.get('F2', 0))
    transition_band = float(specs.get('TransitionBand', 0))
    stop_attenuation = float(specs.get('StopBandAttenuation', 0))
    
    print(f"\n=== Test Case 5: BPF Coefficients ===")
    print(f"Filter Type: {filter_type}")
    print(f"Fs={Fs}, F1={F1}, F2={F2}, TransitionBand={transition_band}, StopAttenuation={stop_attenuation}")
    
    h = FIR.fir_band_pass(Fs, F1, F2, transition_band, stop_attenuation)
    
    print(f"Filter length: {len(h)}")
    
    # Use Compare_Signals function - indices centered at 0
    M = (len(h) - 1) // 2
    h_indices = list(range(-M, M + 1))
    h_samples = h.tolist()
    Compare_Signals('test_cases/Testcase 5/BPFCoefficients.txt', h_indices, h_samples)

def test_case_6():
    """Test Case 6: Band Pass Filter Signal Filtering"""
    print(f"\n=== Test Case 6: BPF Signal Filtering ===")
    
    specs = parse_specs('test_cases/Testcase 6/Filter Specifications.txt')
    filter_type = specs.get('FilterType', '').lower()
    Fs = float(specs.get('FS', 0))
    F1 = float(specs.get('F1', 0))
    F2 = float(specs.get('F2', 0))
    transition_band = float(specs.get('TransitionBand', 0))
    stop_attenuation = float(specs.get('StopBandAttenuation', 0))
    
    print(f"Filter Type: {filter_type}")
    print(f"Fs={Fs}, F1={F1}, F2={F2}, TransitionBand={transition_band}, StopAttenuation={stop_attenuation}")
    
    h = FIR.fir_band_pass(Fs, F1, F2, transition_band, stop_attenuation)
    
    print(f"Filter length: {len(h)}")
    
    x_indices, x_values = parse_signal('test_cases/Testcase 6/ecg400.txt')
    print(f"Input signal length: {len(x_values)}")
    
    expected_indices, expected_values = parse_signal('test_cases/Testcase 6/ecg_band_pass_filtered.txt')
    print(f"Expected signal length: {len(expected_values)}")
    
    # Method 1: Convolution
    print("\n[Method 1: Convolution]")
    signal_x = np.column_stack((x_indices, x_values))
    M = (len(h) - 1) // 2
    h_indices = np.arange(-M, M + 1)
    signal_h = np.column_stack((h_indices, h))
    
    result_conv = Convolution.convolve(signal_x, signal_h)
    y_indices_conv = result_conv.signal[:, 0].astype(int).tolist()
    y_values_conv = result_conv.signal[:, 1].tolist()
    print(f"  Output signal length: {len(y_values_conv)}")
    Compare_Signals('test_cases/Testcase 6/ecg_band_pass_filtered.txt', y_indices_conv, y_values_conv)
    
    # Method 2: DFT/IDFT
    print("\n[Method 2: DFT/IDFT]")
    y_values_dft = filter_with_dft_idft(x_values, h)
    first_idx = int(x_indices[0]) + (-M)
    y_indices_dft = list(range(first_idx, first_idx + len(y_values_dft)))
    y_values_dft_list = y_values_dft.tolist()
    print(f"  Output signal length: {len(y_values_dft_list)}")
    Compare_Signals('test_cases/Testcase 6/ecg_band_pass_filtered.txt', y_indices_dft, y_values_dft_list)

def test_case_7():
    """Test Case 7: Band Stop Filter Coefficients"""
    specs = parse_specs('test_cases/Testcase 7/Filter Specifications.txt')    
    filter_type = specs.get('FilterType', '').lower()
    Fs = float(specs.get('FS', 0))
    F1 = float(specs.get('F1', 0))
    F2 = float(specs.get('F2', 0))
    transition_band = float(specs.get('TransitionBand', 0))
    stop_attenuation = float(specs.get('StopBandAttenuation', 0))
    
    print(f"\n=== Test Case 7: BSF Coefficients ===")
    print(f"Filter Type: {filter_type}")
    print(f"Fs={Fs}, F1={F1}, F2={F2}, TransitionBand={transition_band}, StopAttenuation={stop_attenuation}")
    
    h = FIR.fir_band_stop(Fs, F1, F2, transition_band, stop_attenuation)
    
    print(f"Filter length: {len(h)}")
    
    # Use Compare_Signals function - indices centered at 0
    M = (len(h) - 1) // 2
    h_indices = list(range(-M, M + 1))
    h_samples = h.tolist()
    Compare_Signals('test_cases/Testcase 7/BSFCoefficients.txt', h_indices, h_samples)

def test_case_8():
    """Test Case 8: Band Stop Filter Signal Filtering"""
    print(f"\n=== Test Case 8: BSF Signal Filtering ===")
    
    specs = parse_specs('test_cases/Testcase 8/Filter Specifications.txt')
    filter_type = specs.get('FilterType', '').lower()
    Fs = float(specs.get('FS', 0))
    F1 = float(specs.get('F1', 0))
    F2 = float(specs.get('F2', 0))
    transition_band = float(specs.get('TransitionBand', 0))
    stop_attenuation = float(specs.get('StopBandAttenuation', 0))
    
    print(f"Filter Type: {filter_type}")
    print(f"Fs={Fs}, F1={F1}, F2={F2}, TransitionBand={transition_band}, StopAttenuation={stop_attenuation}")
    
    h = FIR.fir_band_stop(Fs, F1, F2, transition_band, stop_attenuation)
    
    print(f"Filter length: {len(h)}")
    
    x_indices, x_values = parse_signal('test_cases/Testcase 8/ecg400.txt')
    print(f"Input signal length: {len(x_values)}")
    
    expected_indices, expected_values = parse_signal('test_cases/Testcase 8/ecg_band_stop_filtered.txt')
    print(f"Expected signal length: {len(expected_values)}")
    
    # Method 1: Convolution
    print("\n[Method 1: Convolution]")
    signal_x = np.column_stack((x_indices, x_values))
    M = (len(h) - 1) // 2
    h_indices = np.arange(-M, M + 1)
    signal_h = np.column_stack((h_indices, h))
    
    result_conv = Convolution.convolve(signal_x, signal_h)
    y_indices_conv = result_conv.signal[:, 0].astype(int).tolist()
    y_values_conv = result_conv.signal[:, 1].tolist()
    print(f"  Output signal length: {len(y_values_conv)}")
    Compare_Signals('test_cases/Testcase 8/ecg_band_stop_filtered.txt', y_indices_conv, y_values_conv)
    
    # Method 2: DFT/IDFT
    print("\n[Method 2: DFT/IDFT]")
    y_values_dft = filter_with_dft_idft(x_values, h)
    first_idx = int(x_indices[0]) + (-M)
    y_indices_dft = list(range(first_idx, first_idx + len(y_values_dft)))
    y_values_dft_list = y_values_dft.tolist()
    print(f"  Output signal length: {len(y_values_dft_list)}")
    Compare_Signals('test_cases/Testcase 8/ecg_band_stop_filtered.txt', y_indices_dft, y_values_dft_list)

def main():
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()
    test_case_7()
    test_case_8()

if __name__ == '__main__':
    main()
