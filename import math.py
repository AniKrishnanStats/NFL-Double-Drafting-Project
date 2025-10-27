import math
import numpy as np
from math import factorial, sqrt, log10

def pi_from_quarter_polygon(T):
    x = np.linspace(0, 1, T + 1)
    y = np.sqrt(1 - x*x)
    dx = 1 / T
    dy = np.diff(y)
    seg = np.hypot(dx, dy)
    return 2 * np.sum(seg)

def pi_from_ramanujan(T):
    s = 0
    for k in range(T):
        num = factorial(4*k) * (1103 + 26390*k)
        den = (factorial(k)**4) * (396**(4*k))
        s += num/den
    inv_pi = (2*sqrt(2)/9801) * s
    return 1/inv_pi

def digits_correct(rel_err):
    if rel_err <= 0: return 16
    return -math.log10(rel_err)

Ts1 = [1, 2, 3, 10, 1000, 1000000]
print("Quarter Polygon Approximation")
print(f"{'T':>10} {'pi_estimate':>15} {'abs_error':>15} {'rel_error':>15} {'digits_correct':>15}")
for T in Ts1:
    pi_hat = pi_from_quarter_polygon(T)
    abs_err = abs(pi_hat - math.pi)
    rel_err = abs_err / math.pi
    digs = digits_correct(rel_err)
    print(f"{T:10d} {pi_hat:15.8f} {abs_err:15.8e} {rel_err:15.8e} {digs:15.2f}")

Ts2 = [1, 2, 3, 10, 1000, 1000000]
print("\nRamanujan Approximation")
print(f"{'T':>10} {'pi_estimate':>15} {'abs_error':>15} {'rel_error':>15} {'digits_correct':>15}")
for T in Ts2:
    pi_hat = pi_from_ramanujan(T)
    abs_err = abs(pi_hat - math.pi)
    rel_err = abs_err / math.pi
    digs = digits_correct(rel_err)
    print(f"{T:10d} {pi_hat:15.12f} {abs_err:15.8e} {rel_err:15.8e} {digs:15.2f}")
