import sys, os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Task6.Correlation import Correlation

# Provided inputs from user request (first few lines)
# 0 2
# 1 1
# 2 0
# 3 0
# 4 3

# 0 3
# 1 2
# 2 1
# 3 1
# 4 5

# Expected Output:
# 0 0.97192739
# 1 0.59160798
# 2 0.38031941
# 3 0.42257713
# 4 0.6761234

# Reconstruct full signals if possible or test with this subset if it's the full signal.
# The user request showed indices 0-4. Let's assume the signal IS length 5 for this test.
s1 = [2, 1, 0, 0, 3]
s2 = [3, 2, 1, 1, 5]

expected = [0.97192739, 0.59160798, 0.38031941, 0.42257713, 0.6761234]

print("Running Correlation with test data...")
result = Correlation.direct_correlation(s1, s2)

print("\nComputed vs Expected:")
all_pass = True
for i, val in enumerate(result):
    print(f"{i}: {val:.8f} (Expected: {expected[i]})")
    if abs(val - expected[i]) > 1e-6:
        all_pass = False

if all_pass:
    print("\nVERIFICATION PASSED")
else:
    print("\nVERIFICATION FAILED")
