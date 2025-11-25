# 🔢 Gauss–Jordan Equation Solver  
*A tiny Python script created out of academic pressure, caffeine, and the refusal to manually eliminate equations ever again.*

This tool solves systems of linear equations using **Gauss–Jordan elimination**, showing every transformation in clean human-readable **equation format** (not scary matrices).  
Just enter equations like:

```

a b c : d

```

…which the script interprets as:

```

a·x₁ + b·x₂ + c·x₃ = d

````

Perfect for students, engineers, or anyone who refuses to suffer through manual elimination at 2 AM.

---

## 🚀 Features

- Accepts **number of variables** and **number of equations**
- Intuitive input format: `a b c : d`
- Displays equations like `3x_1 + 2x_2 = 5`
- Performs:
  - Forward elimination  
  - Backward elimination  
  - Pivot normalization  
- Uses GCD-based scaled operations for cleaner steps  
- Shows **every** transformation using human-readable row operations
- Prints final reduced form + the solution for each variable  

---

## 📂 Why This Exists (The Backstory)

Because solving linear equations by hand is:

- Not fun  
- Not fast  
- Not safe for mental health  

This script exists because:

- One day the assignment was due  
- The matrix was big  
- The clock was ticking  
- And your brain said: "Let Python suffer instead."

Thus, this solver was born.

---

## 🎁 Benefits

- **Crystal clear steps** — see exactly how each equation transforms  
- **Error-proof** — no accidental sign flips or miswritten coefficients  
- **Cleaner than matrices** — equations stay readable  
- **Universal** — works for any number of variables/equations  
- **Student-saver** — especially during mid-semester breakdown season  

---

## 📝 How to Use

Run the script:

```bash
python main.py
````

Follow the prompts:

1. Enter number of variables
2. Enter number of equations
3. Enter each like:

   ```
   1 2 3 : 9
   ```
4. Watch Python do:

   * elimination
   * reverse elimination
   * pivot normalization
   * solution extraction

You sit back and relax.

---

## ⚙️ Notes

* Uses **GCD scaling** to keep numbers manageable
* Outputs readable equations, not cryptic matrix blocks
* Designed for learning + assignments — not hardcore numerical optimization
* Supports integer and decimal coefficients

---

## 📜 Example Input

```
Enter number of variables: 3
Enter number of equations: 3
Enter equation 1 (format: a b c : d): 1 2 3 : 9
Enter equation 2 (format: a b c : d): 2 1 1 : 8
Enter equation 3 (format: a b c : d): 3 -1 2 : 7
```

The script prints every step and ends with:

```
x1 = 2.5714285714285716
x2 = 2.142857142857143
x3 = 0.7142857142857143
```

---

Just tell me! If you have somethong more mathcodical.
