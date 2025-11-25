# =============================
#    GAUSS–JORDAN SOLVER
# =============================

def parse_equation_input(i, n_vars):
    """Read equation in format: a b c : d"""
    while True:
        raw = input(f"Enter equation {i+1} (format: a b c : d): ").strip()
        if ":" not in raw:
            print("Format incorrect. Use: a b c : d")
            continue

        left, right = raw.split(":")
        left = left.strip().split()
        right = right.strip()

        if len(left) != n_vars:
            print(f"You must enter exactly {n_vars} coefficients.")
            continue
        
        try:
            coeffs = list(map(float, left))
            const = float(right)
            return coeffs + [const]
        except:
            print("Only numeric values allowed.")
            continue


def print_equations(m, n_vars):
    """Print current equations as: a_1 x_1 + a_2 x_2 ... = d"""
    for r in range(len(m)):
        eq = ""
        for c in range(n_vars):
            coef = m[r][c]
            
            # Pretty print integer-like floats
            if coef == 0:
                coef = 0
            elif coef.is_integer():
                coef = int(coef)

            eq += f"{coef}x_{c+1} "
            if c != n_vars - 1:
                eq += "+ "
        const = m[r][-1]
        const = int(const) if const.is_integer() else const
        print(f"Eq{r+1}: {eq}= {const}")
    print('=' * 10)


def gcd(a, b):
    """Integer GCD, safe for floats representing integers"""
    a, b = int(a), int(b)
    while b:
        a, b = b, a % b
    return abs(a)


# =============================
#       MAIN PROGRAM
# =============================

# Number of variables
while True:
    try:
        n_vars = int(input("Enter number of variables: "))
        if n_vars > 0:
            break
    except:
        pass
    print("Invalid input. Enter positive integer.")

# Number of equations
while True:
    try:
        n_eq = int(input("Enter number of equations: "))
        if n_eq > 0:
            break
    except:
        pass
    print("Invalid input. Enter positive integer.")


# Read augmented matrix
m = []
for i in range(n_eq):
    m.append(parse_equation_input(i, n_vars))

print("\n================ Initial Equations ================")
print_equations(m, n_vars)

# GAUSS-JORDAN METHOD
rows = n_eq
cols = n_vars + 1

# --- Forward Elimination ---
for i in range(min(rows, n_vars)):
    
    # If pivot is zero, skip pivot column
    if m[i][i] == 0:
        continue

    # Eliminate below
    for j in range(i+1, rows):
        if m[j][i] == 0:
            continue

        g = gcd(m[i][i], m[j][i])
        r2 = m[i][i] / g
        r1 = m[j][i] / g

        print(f"R{j+1} -> {r2}R{j+1} - {r1}R{i+1}")

        for c in range(i, cols):
            m[j][c] = r2*m[j][c] - r1*m[i][c]

    print_equations(m, n_vars)


# --- Backward Elimination ---
for i in range(min(rows, n_vars)-1, -1, -1):
    if m[i][i] == 0:
        continue

    for j in range(i-1, -1, -1):
        if m[j][i] == 0:
            continue

        g = gcd(m[i][i], m[j][i])
        r2 = m[i][i] / g
        r1 = m[j][i] / g

        print(f"R{j+1} -> {r2}R{j+1} - {r1}R{i+1}")

        for c in range(cols):
            m[j][c] = r2*m[j][c] - r1*m[i][c]

    print_equations(m, n_vars)


# --- Normalize pivots to 1 ---
for i in range(min(rows, n_vars)):
    pivot = m[i][i]
    if pivot != 0:
        for c in range(cols):
            m[i][c] /= pivot

print("================ Final Reduced Form ================")
print_equations(m, n_vars)


# --- Extract Solution ---
print("================ Solutions ================")
for i in range(n_vars):
    val = m[i][-1]
    val = int(val) if float(val).is_integer() else val
    print(f"x{i+1} = {val}")
