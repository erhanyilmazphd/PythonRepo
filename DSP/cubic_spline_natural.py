import numpy as np
import bisect
import matplotlib.pyplot as plt


def natural_cubic_spline(x, y):
    """
    Calculates the coefficients a, b, c, d for Natural Cubic Spline interpolation.
    Based on the formulation in Source [2] and [4].

    Args:
        x (array): x-coordinates of data points (must be sorted).
        y (array): y-coordinates of data points.

    Returns:
        matrix: A matrix of shape (n, 4) where each row i contains
                coefficients [ai, bi, ci, di] for the interval [xi, xi+1].
    """
    n = len(x) - 1
    h = np.diff(x)  # Step sizes h_i = x_{i+1} - x_i

    # 1. Initialize the Tridiagonal Matrix System for c_i (second derivative / 2)
    # The system is Ac = z. A is (n+1)x(n+1).
    # Source [2] defines the matrix structure for natural splines.

    A = np.zeros((n + 1, n + 1))
    rhs = np.zeros(n + 1)

    # Natural Boundary Conditions: c_0 = 0 and c_n = 0 [2, 3]
    A[0, 0] = 1.0
    A[n, n] = 1.0

    # Fill the interior rows of the tridiagonal matrix [2]
    # h_{i-1} * c_{i-1} + 2(h_{i-1} + h_i) * c_i + h_i * c_{i+1} = RHS
    for i in range(1, n):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]

        # Right Hand Side calculation [2]
        term1 = (y[i + 1] - y[i]) / h[i]
        term2 = (y[i] - y[i - 1]) / h[i - 1]
        rhs[i] = 3 * (term1 - term2)

    # 2. Solve the linear system for c coefficients
    # In production, a Thomas Algorithm (O(n)) is preferred [2],
    # but numpy.linalg.solve is sufficient for demonstration.
    c = np.linalg.solve(A, rhs)

    # 3. Calculate b_i and d_i based on c_i
    # a_i is simply y_i [1]
    b = np.zeros(n)
    d = np.zeros(n)
    a = y[0:n]  # a_i = y_i for i=0 to n-1

    for i in range(n):
        # Formula from Source [4]: d_i = (c_{i+1} - c_i) / (3h_i)
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])

        # Formula from Source [4]: b_i = (y_{i+1} - y_i)/h_i - h_i(2c_i + c_{i+1})/3
        b[i] = (y[i + 1] - y[i]) / h[i] - (h[i] * (2 * c[i] + c[i + 1])) / 3

    return np.column_stack((a, b, c[:-1], d))


def evaluate_spline(x_val, x_data, coeffs):
    """
    Args:
        x_val (float): The input value to interpolate.
        x_data (array): The sorted known x-coordinates (knots).
        coeffs (matrix): The coefficients matrix [a, b, c, d] for each interval.
    """
    n = len(x_data) - 1

    # Handle boundary conditions (extrapolation or clamping)
    if x_val < x_data[0] or x_val > x_data[n]:
        print("Warning: Value is outside interpolation range.")
        # Clamp to boundaries for this example
        if x_val < x_data[0]: return coeffs
        if x_val > x_data[n]: return coeffs[n - 1] + \
            coeffs[n - 1][7] * (x_data[n] - x_data[n - 1]) + \
            coeffs[n - 1][8] * (x_data[n] - x_data[n - 1]) ** 2 + \
            coeffs[n - 1][9] * (x_data[n] - x_data[n - 1]) ** 3

    # Step 1: Find the interval index i using binary search
    # bisect_right returns the insertion point to maintain order.
    # We subtract 1 to get the interval index where x_i <= x_val.
    i = bisect.bisect_right(x_data, x_val) - 1

    # Ensure i stays within valid bounds (0 to n-1)
    i = max(0, min(i, n - 1))

    # Step 2: Retrieve coefficients and calculate dx
    a, b, c, d = coeffs[i]
    dx = x_val - x_data[i]

    # Step 3: Evaluate the cubic polynomial
    y_val = a + (b * dx) + (c * dx ** 2) + (d * dx ** 3)

    return y_val


# --- Example Usage ---
# Data from Source [5] example: (0, 1), (0.5, -1), (1, 2)
x_data = np.array([0,    0.5, 1,   1.5, 2,    2.5,    3,  3.5,  4,    4.5,   5])
y_data = np.array([1.0, -1.0, 2.0, 4.0, 5.0, -6.0, 12.0, 32.0, 5.0, -12.0, 4.0])

coeffs = natural_cubic_spline(x_data, y_data)
print("Coefficients (a, b, c, d):\n", coeffs)

# Get some x values after Cubic Spline Coefficients are found
x_val = 4.2
y_val = evaluate_spline(x_val, x_data, coeffs)
print(f" (x_val, y_val) = ({x_val}, {y_val})\n")

# Plotting
x_plot = np.linspace(min(x_data), max(x_data), 100)
y_plot = []

for val in x_plot:
    # Find which interval x is in
    idx = np.searchsorted(x_data, val, side='right') - 1
    idx = np.clip(idx, 0, len(coeffs) - 1)

    xi = x_data[idx]
    a, b, c, d = coeffs[idx]

    # Evaluate S_i(x) = a + b(dx) + c(dx)^2 + d(dx)^3 [1]
    dx = val - xi
    y_val = a + b * dx + c * dx ** 2 + d * dx ** 3
    y_plot.append(y_val)

plt.plot(x_data, y_data, 'ro', label='Data Points')
plt.plot(x_plot, y_plot, 'b-', label='Natural Cubic Spline')
plt.legend()
plt.show()


