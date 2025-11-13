#!/usr/bin/env python
# coding: utf-8
# %%

# %%

def ReadSignalFile(file_name):
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
    return expected_indices,expected_samples


# %%


def AveragingTest(Your_indices, Your_samples):
    file_name = "Task4/testcases/Moving Average testcases/MovingAvg_out1.txt"  # path of the averaging output file
    expected_indices, expected_samples = ReadSignalFile(file_name)
    if (len(expected_samples) != len(Your_samples)) or (len(expected_indices) != len(Your_indices)):
        print("Averaging Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i] != expected_indices[i]):
            print("Averaging Test case failed, your signal have different indices from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Averaging Test case failed, your signal have different values from the expected one")
            return
    print("Averaging Test case passed successfully")


# %%


def SharpeningTest(Your_indices, Your_samples):
    file_name = "Task4/testcases/Derivative testcases/1st_derivative_out.txt"  # path of the sharpening (1st derivative) output file
    expected_indices, expected_samples = ReadSignalFile(file_name)
    if (len(expected_samples) != len(Your_samples)) or (len(expected_indices) != len(Your_indices)):
        print("Sharpening Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i] != expected_indices[i]):
            print("Sharpening Test case failed, your signal have different indices from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Sharpening Test case failed, your signal have different values from the expected one")
            return
    print("Sharpening Test case passed successfully")


# %%


def ConvolutionTest(Your_indices, Your_samples):
    file_name = "Task4/testcases/Convolution testcases/Conv_output.txt"  # path of the convolution output file
    expected_indices, expected_samples = ReadSignalFile(file_name)
    if (len(expected_samples) != len(Your_samples)) or (len(expected_indices) != len(Your_indices)):
        print("Convolution Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i] != expected_indices[i]):
            print("Convolution Test case failed, your signal have different indices from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Convolution Test case failed, your signal have different values from the expected one")
            return
    print("Convolution Test case passed successfully")


# %%


def AveragingTest2(Your_indices, Your_samples):
    file_name = "Task4/testcases/Moving Average testcases/MovingAvg_out2.txt"  # path of the second averaging output file
    expected_indices, expected_samples = ReadSignalFile(file_name)
    if (len(expected_samples) != len(Your_samples)) or (len(expected_indices) != len(Your_indices)):
        print("Averaging Test case 2 failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i] != expected_indices[i]):
            print("Averaging Test case 2 failed, your signal have different indices from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Averaging Test case 2 failed, your signal have different values from the expected one")
            return
    print("Averaging Test case 2 passed successfully")


# %%


def SharpeningTest2(Your_indices, Your_samples):
    file_name = "Task4/testcases/Derivative testcases/2nd_derivative_out.txt"  # path of the second derivative (sharpening) output file
    expected_indices, expected_samples = ReadSignalFile(file_name)
    if (len(expected_samples) != len(Your_samples)) or (len(expected_indices) != len(Your_indices)):
        print("Sharpening Test case 2 failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i] != expected_indices[i]):
            print("Sharpening Test case 2 failed, your signal have different indices from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Sharpening Test case 2 failed, your signal have different values from the expected one")
            return
    print("Sharpening Test case 2 passed successfully")


# %%
