
import numpy as np
import random
print("=== TASK 1: 4x4 MATRIX ANALYSIS ===\n")

# Step 1: Create 4x4 matrix with random integers 1-100
matrix = np.random.randint(1, 101, size=(4, 4))
print("1. 4x4 Matrix:")
print(matrix)
print()

# Step 2: Maximum value
max_value = np.max(matrix)
print(f"2. Maximum value: {max_value}")

# Step 3: Minimum value
min_value = np.min(matrix)
print(f"3. Minimum value: {min_value}")

# Step 4: Mean (average)
mean_value = np.mean(matrix)
print(f"4. Mean: {mean_value:.2f}")

# Step 5: Total sum
total_sum = np.sum(matrix)
print(f"5. Total sum: {total_sum}")
print()

# Step 6: Extract first row and last column
first_row = matrix[0]        # Simplified
last_column = matrix[:, -1]
print("6. Extracted elements:")
print(f"   First row:    {first_row}")
print(f"   Last column:  {last_column}")