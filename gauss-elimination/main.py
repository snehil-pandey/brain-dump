rows = cols = 0

# inputing number of rows
while rows <= 0:
    try:
        rows = int(input('Enter number of rows: '))
    except:
        print('rows cannot be less than 1')

# inputing number of columns
while cols <= 0:
    try:
        cols = int(input('Enter number of columns: '))
    except:
        print('columns cannot be less than 1')

m = [[None] * cols for _ in range(rows)]  # Matrix placeholder

# inputing the elements of matrix
i = 0
w = 3  # default width
while i < rows:
    tmp = input(f'Enter {i+1}th row elements separated by space: ').split()
    if len(tmp) != cols:
        print('please enter correctly like: 1 2 3 4')
        continue
    try:
        m[i] = list(map(float, tmp))
    except:
        print('Only numbers allowed.')
        continue
    w = max(w, max(len(x) for x in tmp))
    i += 1


# ------------ WIDTH RECOMPUTE FUNCTION ------------
def compute_width(matrix):
    width = 1
    for row in matrix:
        for val in row:
            if val == 0:
                s = "0"
            elif float(val).is_integer():
                s = str(int(val))
            else:
                s = str(val)
            width = max(width, len(s))
    return width


# ------------ PRINT MATRIX FUNCTION ------------
def print_matrix(matrix):
    width = compute_width(matrix)  # dynamic width

    for row in matrix:
        line = ""
        for val in row:
            if val == 0:
                s = "0"
            elif float(val).is_integer():
                s = str(int(val))
            else:
                s = str(val)
            line += " " * (width - len(s) + 1) + s
        print(line)
    print()


# ------------ START PRINT ------------
print("=" * (cols * w * 2))
print("Initial Matrix:")
print_matrix(m)
print("=" * (cols * w * 2))


# ------------ GCD FUNCTION ------------
def gcd(a, b):
    mod = a % b
    if mod == 0:
        return b
    else:
        return gcd(b, mod)


# ------------ ROW OPERATIONS ------------
i = 0
while i < min(rows, cols) - 1:
    j = i + 1
    while j < rows:
        if m[j][i] == 0:
            j += 1
            continue

        factor = gcd(m[i][i], m[j][i])
        r2_coeff = m[i][i] / factor
        r1_coeff = m[j][i] / factor

        k = i
        while k < cols:
            m[j][k] = r2_coeff * m[j][k] - r1_coeff * m[i][k]
            k += 1

        print(f'R{j+1} -> {r2_coeff}R{j+1} - {r1_coeff}R{i+1}')
        j += 1

    print_matrix(m)
    i += 1
    if i != rows:
        print("=" * (cols * w))


# ------------ FINAL PRINT ------------
print("=" * (cols * w * 2))
print("Final Echelon Form:")
print_matrix(m)
print("=" * (cols * w * 2))
