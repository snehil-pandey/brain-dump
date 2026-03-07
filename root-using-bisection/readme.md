# 🔍 Root Finder - Bisection Method
*A tiny script born from numerical methods assignments and the painful reality of repetitive calculator work.*

This tool performs the **Bisection Method** for solving nonlinear equations and prints clean, step-by-step iterations just like you would write in a numerical methods table.

Instead of manually calculating midpoints and function values again and again, the script automates the process and shows each iteration clearly.

---

## 🚀 Features
- Accepts **any mathematical equation** using `x`
- Supports **NumPy functions** like `sin`, `cos`, `exp`, etc.
- Takes custom interval `[a, b]`
- Automatically checks **valid interval conditions**
- Prints **iteration-by-iteration table**
- Stops when the root is sufficiently accurate

---

## 📂 Why This Exists (The Origin Story)

Because solving Bisection Method problems the traditional way looks like this:

1. Open calculator  
2. Compute midpoint  
3. Substitute into the equation  
4. Compute the function value  
5. Decide the next interval  
6. Write the entire row in the table  
7. Repeat **10–20 times**

And somewhere around iteration 12, you realize you typed one wrong number and the entire table collapses.

What should be a simple algorithm turns into **endless calculator punching and table drawing**.

So this script was created to:

- Avoid repetitive calculator work  
- Generate iteration tables instantly  
- Prevent arithmetic mistakes  
- Speed up assignment solving  
- Focus on understanding the method rather than fighting the calculator

---

## 🎁 Benefits

- **Fast**: Finds roots in seconds  
- **Accurate**: Eliminates manual calculation errors  
- **Educational**: Shows every iteration clearly  
- **Flexible**: Works with many types of equations  
- **Assignment-friendly**: Easy to copy results into tables

---

## 📝 How to Use

Run the script with Python:

```bash
python main.py
