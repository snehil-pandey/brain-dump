# 🧮 NumberSystem — A Custom Positional Number Engine

*A project that started from basic base conversion logic in an EC class and somehow evolved into building an entire custom numeric datatype.*

This project is a fully object-oriented **custom number system engine** capable of:

* Converting between arbitrary bases
* Supporting custom digit representations
* Performing arithmetic directly on numbers from different bases
* Handling negative numbers and fractional values
* Behaving almost like Python’s built-in numeric types

What began as a tiny experiment with base conversion slowly turned into an obsession with building a reusable and extensible number system architecture.

---

# 🚀 Features

* Convert between **any base ≥ 2**
* Supports:

  * Positive numbers
  * Negative numbers
  * Fractional / decimal values
* Arithmetic operations:

  * Addition
  * Subtraction
  * Multiplication
  * Division
  * Floor division
  * Modulo
  * Exponentiation
* Comparison operators:

  * `==`
  * `!=`
  * `<`
  * `>`
  * `<=`
  * `>=`
* Unary operators:

  * `+x`
  * `-x`
  * `abs(x)`
* Assignment operators:

  * `+=`
  * `-=`
  * `*=`
  * `/=`
  * `//=`
  * `%=`
  * `**=`
* Reverse operations:

  * `5 + NumberSystem(...)`
  * `2 * NumberSystem(...)`
* Hash support:

  * usable inside sets
  * usable as dictionary keys
* Input validation system
* Internal conversion caching optimization
* Fully object-oriented implementation

---

# 📂 The Origin Story

This entire thing started during an EC class while learning about number systems and base conversions.

At first it was just:

* converting from base10 to another base
* converting back to base10

Nothing serious.

Later I went to the lab and wrote a crude implementation that only supported:

* `0-9`
* `A-Z`

which meant it was effectively limited to base36.

But then I ran into a weird problem:

What happens after base36?

Most implementations stop there.

I didn’t want that.

So I created my own representation style for larger digits:

```text
(45)
(72)
(128)
```

instead of inventing random symbols.

That single decision completely changed the direction of the project.

Because once arbitrary digit representation existed, the project stopped being just “base conversion code”.

Then came:

* negative numbers
* fractional values
* arithmetic operators
* comparisons
* hashing
* assignment operators
* validation systems
* caching optimizations

And eventually the project evolved into building a complete custom number datatype system.

At some point I realized:

> I’m no longer converting numbers between bases.

> I’m trying to create my own number system legacy.

And that’s how this giant block of code happened.

---

# 🧠 Core Idea

Most base conversion programs work like tiny utilities.

Input:

```text
1010₂
```

Output:

```text
10₁₀
```

Done.

This project goes much further.

The goal here was to make numbers from arbitrary bases behave like actual Python numeric objects.

Example:

```python
a = NumberSystem("101", 2)
b = NumberSystem("3", 10)

print(a + b)
print(a * b)
print(a / b)
```

Instead of merely converting numbers, the system allows:

* operations between different bases
* automatic conversions
* object-oriented arithmetic
* reusable numeric behavior

---

# 🏗 Architecture Overview

The engine internally follows this workflow:

```text
Current Base
      ↓
Convert to Base10
      ↓
Perform Operation
      ↓
Convert Back To Original Base
```

This approach keeps the implementation:

* clean
* understandable
* extensible

instead of implementing separate arithmetic logic for every possible base.

---

# ⚡ Performance Optimization

Initially every operation repeatedly recalculated conversions.

Example:

```python
a+b
a-b
a*b
```

Each operation internally called:

```python
toBase10()
```

again and again.

So a caching system was introduced.

Now:

* first conversion computes normally
* future conversions instantly reuse cached values

This significantly reduces unnecessary repeated work.

---

# 🛡 Input Validation

During testing I noticed malformed inputs could silently break behavior.

Examples:

```text
1..2
--101
()
1A-
```

So strict validation logic was added to:

* reject invalid syntax early
* fail clearly
* prevent hidden bugs later

This made the system much more stable.

---

# 🎁 Why This Project Is Interesting

This project unintentionally touches multiple areas simultaneously:

* Number Systems
* Object-Oriented Programming
* Operator Overloading
* Parsing
* Internal Representations
* Arithmetic Systems
* Validation Architectures
* Performance Optimization
* Python Data Model

So even though it started from a simple educational topic, it slowly became a much deeper software design experiment.

---

# 🛠 How To Use

Run the file directly:

```bash
python main.py
```

The file already contains:

* demonstrations
* arithmetic examples
* conversion examples
* validation tests
* hashing tests
* assignment operator tests
* cache demonstrations

---

# 🧪 Example Usage

## Create Numbers

```python
a = NumberSystem("101", 2)
b = NumberSystem("1A", 16)
```

---

## Convert Bases

```python
print(a.toBase10())
print(b.toBaseN(2))
```

---

## Arithmetic

```python
print(a + b)
print(a - b)
print(a * b)
print(a / b)
```

---

## Comparisons

```python
print(a == b)
print(a > b)
```

---

## Assignment Operations

```python
a += NumberSystem("1", 10)
a *= NumberSystem("10", 10)
```

---

# 📌 Current Limitations

The engine still internally uses Python `float()` for arithmetic.

This means floating-point precision limitations still exist for certain values.

Example:

```python
0.1 + 0.2
```

may still produce:

```python
0.30000000000000004
```

A future improvement would be replacing `float` with:

```python
Decimal
```

for higher precision arithmetic.

---

# 🔮 Possible Future Improvements

* Decimal precision system
* Repeating fraction detection
* Rational number support
* Bitwise operations
* Scientific notation support
* Direct base arithmetic without converting to base10 first
* Complex number support
* Symbolic math extensions

~~ofc I won't implement as a hint of memory to my dump style coding cuz it's not a project~~

---

# 🏁 Final Note

This project started from:

> “Let me automate base conversion.”

and somehow evolved into:

> “What if I build my own fully functional number system datatype?”

That escalation was absolutely not planned.
