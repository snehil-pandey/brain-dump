import numpy as np

def get_equation():
    print("Enter your equation using 'x' as the variable.")
    print("Examples:")
    print("  x**3 - 4*x - 9")
    print("  np.sin(x) - 0.5")
    print("  np.exp(x) - 3*x\n")
    expr = input("f(x) = ")
    def f(x):
        return eval(expr)
    return f, expr

def bisect_x(f, a, b, iteration=1):
    m = (a + b) / 2
    r = f(m)
    print(f'Iteration {iteration}: a={a:.6f}, b={b:.6f}, x_0={m:.6f}, f(x_0)={r:.6f}')
    if abs(r) < 1e-6:
        return m
    elif r > 0:
        return bisect_x(f, a, m, iteration + 1)
    else:
        return bisect_x(f, m, b, iteration + 1)

print("=== Bisection Method ===\n")

# Get equation
while True:
    try:
        f, expr = get_equation()
        f(1.0)  # test the equation
        break
    except Exception as e:
        print(f"Invalid equation: {e}. Try again.\n")

# Get a and b
while True:
    try:
        a = float(input("Enter value for a: "))
        b = float(input("Enter value for b: "))

        if f(a) * f(b) > 0:
            print("Invalid interval: f(a) and f(b) must have opposite signs. Try again.\n")
            continue
        break
    except ValueError:
        print("Please enter valid numbers.\n")

print(f'\nSolving: f(x) = {expr}')
print(f'Interval: [{a}, {b}]\n')
root = bisect_x(f, a, b)
print(f'\nApproximate root: {root:.6f}')
