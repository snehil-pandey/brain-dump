class NumberSystem:

    # ---------------------------------------------------------
    # CONSTRUCTOR
    # ---------------------------------------------------------

    def __init__(self, number, base):

        # Every positional number system needs minimum base 2
        # Base 1 behaves differently (unary system)
        if base < 2:
            raise ValueError("Base must be >= 2")

        # Store internally as uppercase string
        # Why uppercase?
        # So:
        #   a == A
        # and representation stays standardized.
        self.number = str(number).upper()

        self.base = base

        # Split into usable digit tokens
        # Example:
        #   "1A(45).B"
        # becomes:
        #   ['1','A','(45)','.','B']
        self.digits = self.__splitDigits()

        # -------------------------------------------------
        # PERFORMANCE CACHE
        # -------------------------------------------------

        """
        Initially I noticed something inefficient:

        Every arithmetic operation repeatedly called:
            toBase10()

        That means same conversion work
        happening again and again.

        Example:
            a+b
            a-b
            a*b

        each recalculating full decimal conversion.

        So we cache computed result.

        First conversion:
            compute + store

        Next conversions:
            instantly reuse.

        Classic optimization:
            memoization / caching
        """

        self.__base10_cache = None

        # Validate after parsing
        self.__validateNumber()

    # ---------------------------------------------------------
    # STRING REPRESENTATION
    # ---------------------------------------------------------

    def __repr__(self):
        return f"[{self.number}]_{self.base}"

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------

    def __valueToChar(self, value):

        """
        Convert integer value -> printable digit

        0-9    -> 0-9
        10-35  -> A-Z
        >35    -> (value)

        Why brackets?
        Because bases > 36 need multi-char digits.

        Example:
            49 -> "(49)"
        """

        if 0 <= value <= 9:
            return str(value)

        if 10 <= value <= 35:
            return chr(ord('A') + value - 10)

        return f"({value})"

    def __charToValue(self, ch):

        """
        Reverse operation:
            digit -> integer value
        """

        if ch.isdigit():
            return int(ch)

        if len(ch) == 1 and ch.isalpha():
            return ord(ch.upper()) - ord('A') + 10

        if ch.startswith("(") and ch.endswith(")"):
            return int(ch[1:-1])

        raise ValueError(f"Invalid digit: {ch}")

    def __splitDigits(self):

        """
        Splits safely into digit tokens.

        Needed because:
            "(45)"
        should become ONE digit.

        Also preserves:
            '.'
            '-'
        """

        result = []
        i = 0

        while i < len(self.number):

            # Multi-character digit
            if self.number[i] == "(":

                j = self.number.find(")", i)

                if j == -1:
                    raise ValueError("Missing ')'")

                result.append(
                    self.number[i:j + 1]
                )

                i = j + 1

            else:

                result.append(self.number[i])
                i += 1

        return result

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def __validateNumber(self):

        """
        Initially malformed inputs like:

            --1A
            1..2
            1A-
            ()

        could behave unpredictably.

        Real numeric systems reject bad syntax early.

        Goal:
            fail fast,
            fail clearly.
        """

        num = self.number

        # Empty invalid
        if len(num) == 0:
            raise ValueError("Empty number")

        # Multiple negatives invalid
        if num.count("-") > 1:
            raise ValueError(
                "Multiple negative signs"
            )

        # '-' only allowed at start
        if "-" in num and not num.startswith("-"):
            raise ValueError(
                "Negative sign only allowed at beginning"
            )

        # Multiple decimals invalid
        if num.count(".") > 1:
            raise ValueError(
                "Multiple decimal points not allowed"
            )

        # Empty brackets invalid
        if "()" in num:
            raise ValueError(
                "Empty bracket digit invalid"
            )

        # Validate digits
        for digit in self.digits:

            if digit in [".", "-"]:
                continue

            value = self.__charToValue(digit)

            if value >= self.base:
                raise ValueError(
                    f"Digit {digit} invalid for base {self.base}"
                )

    # ---------------------------------------------------------
    # BASE -> BASE10
    # ---------------------------------------------------------

    def toBase10(self):

        # -------------------------------------------------
        # CACHE CHECK
        # -------------------------------------------------

        """
        If conversion already computed once,
        instantly return cached version.

        Avoids repeated expensive work.
        """

        if self.__base10_cache is not None:
            return self.__base10_cache

        negative = False

        num = self.number

        # Handle sign
        if num.startswith("-"):
            negative = True
            num = num[1:]

        # Split integer/fraction
        if "." in num:
            integerPart, fractionalPart = num.split(".")
        else:
            integerPart = num
            fractionalPart = ""

        # ---------------- INTEGER PART ----------------

        result = 0

        intDigits = NumberSystem(
            integerPart,
            self.base
        ).digits

        for digitChar in intDigits:

            digit = self.__charToValue(digitChar)

            result = result * self.base + digit

        # ---------------- FRACTIONAL PART ----------------

        fractionalResult = 0

        if fractionalPart != "":

            fracDigits = NumberSystem(
                fractionalPart,
                self.base
            ).digits

            power = -1

            for digitChar in fracDigits:

                digit = self.__charToValue(digitChar)

                fractionalResult += (
                    digit * (self.base ** power)
                )

                power -= 1

        final = result + fractionalResult

        if negative:
            final *= -1

        resultObject = NumberSystem(
            str(final),
            10
        )

        # Store cache
        self.__base10_cache = resultObject

        return resultObject

    # ---------------------------------------------------------
    # BASE10 -> TARGET BASE
    # ---------------------------------------------------------

    def fromBase10(self, targetBase, precision=10):

        if targetBase < 2:
            raise ValueError("Base must be >= 2")

        if self.base != 10:
            raise ValueError(
                "fromBase10() only works from base10"
            )

        value = float(self.number)

        negative = value < 0

        value = abs(value)

        integerPart = int(value)

        fractionalPart = value - integerPart

        # ---------------- INTEGER ----------------

        if integerPart == 0:

            intDigits = ["0"]

        else:

            intDigits = []

            while integerPart > 0:

                remainder = integerPart % targetBase

                intDigits.append(
                    self.__valueToChar(remainder)
                )

                integerPart //= targetBase

            intDigits.reverse()

        # ---------------- FRACTION ----------------

        fracDigits = []

        count = 0

        while fractionalPart > 0 and count < precision:

            fractionalPart *= targetBase

            digit = int(fractionalPart)

            fracDigits.append(
                self.__valueToChar(digit)
            )

            fractionalPart -= digit

            count += 1

        # Build final string

        result = "".join(intDigits)

        if fracDigits:
            result += "." + "".join(fracDigits)

        if negative:
            result = "-" + result

        return NumberSystem(result, targetBase)

    # ---------------------------------------------------------
    # GENERIC CONVERSION
    # ---------------------------------------------------------

    def toBaseN(self, newBase, precision=10):

        """
        Universal conversion strategy:

            current base
                ↓
            base10
                ↓
            target base
        """

        base10 = self.toBase10()

        return base10.fromBase10(
            newBase,
            precision
        )

    # ---------------------------------------------------------
    # ARITHMETIC OPERATIONS
    # ---------------------------------------------------------

    def __add__(self, other):

        a = float(self.toBase10().number)
        b = float(other.toBase10().number)

        return NumberSystem(
            a + b,
            10
        ).toBaseN(self.base)

    def __sub__(self, other):

        a = float(self.toBase10().number)
        b = float(other.toBase10().number)

        return NumberSystem(
            a - b,
            10
        ).toBaseN(self.base)

    def __mul__(self, other):

        a = float(self.toBase10().number)
        b = float(other.toBase10().number)

        return NumberSystem(
            a * b,
            10
        ).toBaseN(self.base)

    def __truediv__(self, other):

        a = float(self.toBase10().number)
        b = float(other.toBase10().number)

        if b == 0:
            raise ZeroDivisionError(
                "Division by zero not allowed"
            )

        return NumberSystem(
            a / b,
            10
        ).toBaseN(self.base)

    def __floordiv__(self, other):

        a = float(self.toBase10().number)
        b = float(other.toBase10().number)

        if b == 0:
            raise ZeroDivisionError(
                "Division by zero not allowed"
            )

        return NumberSystem(
            a // b,
            10
        ).toBaseN(self.base)

    def __mod__(self, other):

        a = float(self.toBase10().number)
        b = float(other.toBase10().number)

        if b == 0:
            raise ZeroDivisionError(
                "Modulo by zero not allowed"
            )

        return NumberSystem(
            a % b,
            10
        ).toBaseN(self.base)

    def __pow__(self, other):

        a = float(self.toBase10().number)
        b = float(other.toBase10().number)

        return NumberSystem(
            a ** b,
            10
        ).toBaseN(self.base)

    # ---------------------------------------------------------
    # UNARY OPERATORS
    # ---------------------------------------------------------

    def __neg__(self):

        value = -float(
            self.toBase10().number
        )

        return NumberSystem(
            value,
            10
        ).toBaseN(self.base)

    def __pos__(self):

        value = float(
            self.toBase10().number
        )

        return NumberSystem(
            value,
            10
        ).toBaseN(self.base)

    def __abs__(self):

        value = abs(
            float(self.toBase10().number)
        )

        return NumberSystem(
            value,
            10
        ).toBaseN(self.base)

    # ---------------------------------------------------------
    # COMPARISONS
    # ---------------------------------------------------------

    def __eq__(self, other):

        return (
            float(self.toBase10().number)
            ==
            float(other.toBase10().number)
        )

    def __ne__(self, other):

        return not self.__eq__(other)

    def __lt__(self, other):

        return (
            float(self.toBase10().number)
            <
            float(other.toBase10().number)
        )

    def __le__(self, other):

        return (
            float(self.toBase10().number)
            <=
            float(other.toBase10().number)
        )

    def __gt__(self, other):

        return (
            float(self.toBase10().number)
            >
            float(other.toBase10().number)
        )

    def __ge__(self, other):

        return (
            float(self.toBase10().number)
            >=
            float(other.toBase10().number)
        )

    # ---------------------------------------------------------
    # HASH SUPPORT
    # ---------------------------------------------------------

    """
    Hashing allows object usage inside:
        - sets
        - dictionary keys

    Important rule:
        equal objects must produce equal hash.

    So:
        [101]_2
        [5]_10

    must hash identically.
    """

    def __hash__(self):

        return hash(
            float(self.toBase10().number)
        )

    # ---------------------------------------------------------
    # TYPE CONVERSIONS
    # ---------------------------------------------------------

    def __int__(self):

        return int(
            float(self.toBase10().number)
        )

    def __float__(self):

        return float(
            self.toBase10().number
        )

    # ---------------------------------------------------------
    # REVERSE OPERATORS
    # ---------------------------------------------------------

    def __radd__(self, other):
        return NumberSystem(other, 10) + self

    def __rsub__(self, other):
        return NumberSystem(other, 10) - self

    def __rmul__(self, other):
        return NumberSystem(other, 10) * self

    def __rtruediv__(self, other):
        return NumberSystem(other, 10) / self

    def __rfloordiv__(self, other):
        return NumberSystem(other, 10) // self

    def __rmod__(self, other):
        return NumberSystem(other, 10) % self

    def __rpow__(self, other):
        return NumberSystem(other, 10) ** self

    # ---------------------------------------------------------
    # ASSIGNMENT OPERATORS
    # ---------------------------------------------------------

    """
    Allows:

        +=
        -=
        *=
        /=
        //=
        %=
        **=

    Without these,
    Python silently creates new object.

    With these,
    datatype behaves naturally like built-in numbers.
    """

    def __iadd__(self, other):

        result = self + other

        self.number = result.number
        self.base = result.base
        self.digits = result.digits

        return self

    def __isub__(self, other):

        result = self - other

        self.number = result.number
        self.base = result.base
        self.digits = result.digits

        return self

    def __imul__(self, other):

        result = self * other

        self.number = result.number
        self.base = result.base
        self.digits = result.digits

        return self

    def __itruediv__(self, other):

        result = self / other

        self.number = result.number
        self.base = result.base
        self.digits = result.digits

        return self

    def __ifloordiv__(self, other):

        result = self // other

        self.number = result.number
        self.base = result.base
        self.digits = result.digits

        return self

    def __imod__(self, other):

        result = self % other

        self.number = result.number
        self.base = result.base
        self.digits = result.digits

        return self

    def __ipow__(self, other):

        result = self ** other

        self.number = result.number
        self.base = result.base
        self.digits = result.digits

        return self


# ---------------------------------------------------------
# TESTING
# ---------------------------------------------------------
print("\n" + "="*70)
print("NUMBER SYSTEM ENGINE TESTING")
print("="*70)

# ---------------------------------------------------------
# BASIC CONVERSION TESTS
# ---------------------------------------------------------

print("\n" + "-"*70)
print("1. BASE CONVERSION TESTS")
print("-"*70)

x = NumberSystem("-1A(10).5", 16)

print("\nOriginal Number:")
print(f"    Number : {x.number}")
print(f"    Base   : {x.base}")
print(f"    Object : {x}")

print("\nDigit Parsing:")
print(f"    Parsed Tokens : {x.digits}")

print("\nConversion To Base10:")
print(f"    {x}  --->  {x.toBase10()}")

print("\nConversion To Binary:")
binaryVersion = x.toBaseN(2)
print(f"    {x}  --->  {binaryVersion}")

print("\nConversion To Base80:")
base80Version = x.toBaseN(80)
print(f"    {x}  --->  {base80Version}")

print("\nConversion To Base50:")
base50Version = x.toBaseN(50)
print(f"    {x}  --->  {base50Version}")

# ---------------------------------------------------------
# ARITHMETIC TESTS
# ---------------------------------------------------------

print("\n" + "-"*70)
print("2. ARITHMETIC OPERATIONS")
print("-"*70)

a = NumberSystem("101", 2)      # 5
b = NumberSystem("3", 10)       # 3

print("\nOperands:")
print(f"    a = {a}  -> decimal {a.toBase10()}")
print(f"    b = {b}  -> decimal {b.toBase10()}")

print("\nAddition:")
print(f"    {a} + {b} = {a+b}")

print("\nSubtraction:")
print(f"    {a} - {b} = {a-b}")

print("\nMultiplication:")
print(f"    {a} * {b} = {a*b}")

print("\nTrue Division:")
print(f"    {a} / {b} = {a/b}")

print("\nFloor Division:")
print(f"    {a} // {b} = {a//b}")

print("\nModulo:")
print(f"    {a} % {b} = {a%b}")

print("\nExponentiation:")
print(f"    {a} ** {b} = {a**b}")

# ---------------------------------------------------------
# UNARY OPERATION TESTS
# ---------------------------------------------------------

print("\n" + "-"*70)
print("3. UNARY OPERATIONS")
print("-"*70)

y = NumberSystem("-10.5", 10)

print("\nOriginal:")
print(f"    y = {y}")

print("\nUnary Negative:")
print(f"    -y = {-y}")

print("\nUnary Positive:")
print(f"    +y = {+y}")

print("\nAbsolute Value:")
print(f"    abs(y) = {abs(y)}")

# ---------------------------------------------------------
# COMPARISON TESTS
# ---------------------------------------------------------

print("\n" + "-"*70)
print("4. COMPARISON OPERATIONS")
print("-"*70)

p = NumberSystem("101", 2)      # 5
q = NumberSystem("5", 10)       # 5

print("\nOperands:")
print(f"    p = {p}")
print(f"    q = {q}")

print("\nEquality:")
print(f"    p == q  ->  {p == q}")

print("\nInequality:")
print(f"    p != q  ->  {p != q}")

print("\nGreater Than:")
print(f"    p > [2]_10  ->  {p > NumberSystem('2',10)}")

print("\nLess Than:")
print(f"    p < [10]_10 ->  {p < NumberSystem('10',10)}")

# ---------------------------------------------------------
# REVERSE OPERATION TESTS
# ---------------------------------------------------------

print("\n" + "-"*70)
print("5. REVERSE OPERATIONS")
print("-"*70)

r = NumberSystem("101", 2)

print("\nOperand:")
print(f"    r = {r}")

print("\nReverse Addition:")
print(f"    5 + r = {5 + r}")

print("\nReverse Subtraction:")
print(f"    10 - r = {10 - r}")

print("\nReverse Multiplication:")
print(f"    2 * r = {2 * r}")

print("\nReverse Division:")
print(f"    20 / r = {20 / r}")

print("\nReverse Power:")
print(f"    2 ** r = {2 ** r}")

# ---------------------------------------------------------
# ASSIGNMENT OPERATOR TESTS
# ---------------------------------------------------------

print("\n" + "-"*70)
print("6. ASSIGNMENT OPERATORS")
print("-"*70)

z = NumberSystem("101", 2)

print("\nInitial Value:")
print(f"    z = {z}")

print("\nApplying += 1")
z += NumberSystem("1", 10)
print(f"    z = {z}")

print("\nApplying *= 10")
z *= NumberSystem("10", 10)
print(f"    z = {z}")

print("\nApplying -= 1")
z -= NumberSystem("1", 10)
print(f"    z = {z}")

print("\nApplying /= 10")
z /= NumberSystem("10", 10)
print(f"    z = {z}")

# ---------------------------------------------------------
# HASHING TESTS
# ---------------------------------------------------------

print("\n" + "-"*70)
print("7. HASHING / SET BEHAVIOR")
print("-"*70)

h1 = NumberSystem("101", 2)
h2 = NumberSystem("5", 10)

print("\nObjects:")
print(f"    h1 = {h1}")
print(f"    h2 = {h2}")

print("\nHashes:")
print(f"    hash(h1) = {hash(h1)}")
print(f"    hash(h2) = {hash(h2)}")

print("\nSet Behavior:")
print("""
    Since both represent same numeric value,
    set should keep only one unique element.
""")

s = {h1, h2}

print(f"    Resulting Set = {s}")

# ---------------------------------------------------------
# VALIDATION TESTS
# ---------------------------------------------------------

print("\n" + "-"*70)
print("8. INPUT VALIDATION TESTS")
print("-"*70)

print("\nCase 1: Multiple Decimal Points")

try:
    NumberSystem("1..2", 10)

except Exception as e:
    print(f"    Error -> {e}")

print("\nCase 2: Multiple Negative Signs")

try:
    NumberSystem("--101", 2)

except Exception as e:
    print(f"    Error -> {e}")

print("\nCase 3: Invalid Digit For Base")

try:
    NumberSystem("2", 2)

except Exception as e:
    print(f"    Error -> {e}")

print("\nCase 4: Empty Bracket Digit")

try:
    NumberSystem("()", 10)

except Exception as e:
    print(f"    Error -> {e}")

# ---------------------------------------------------------
# CACHE DEMONSTRATION
# ---------------------------------------------------------

print("\n" + "-"*70)
print("9. CACHE OPTIMIZATION DEMO")
print("-"*70)

cacheTest = NumberSystem("ABCDEF", 16)

print("""
First conversion:
    conversion actually computed

Second conversion:
    cached result reused
""")

print("First Call:")
print(cacheTest.toBase10())

print("\nSecond Call:")
print(cacheTest.toBase10())

print("\n" + "="*70)
print("ALL TESTS COMPLETED")
print("="*70)
