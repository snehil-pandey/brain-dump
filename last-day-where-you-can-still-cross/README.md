# Last Day to Cross a Flooded Grid &mdash; My Thinking Process

This is my step-by-step explanation on how I tackled the "Last Day to Cross" problem. It's a grid where cells flood day by day, and I need to find the last day you can walk from top row to bottom row on land (4 directions: up/down/left/right).  

## Problem Quick Recap
- Grid: `row` x `col`, starts all land.
- `cells[i]`: cell that floods on day `i+1` (1-based rows/cols).
- Goal: Last day where top row connects to bottom row via land paths.
- Constraints: Up to 200 rows/cols, 40k cells &rarr; need efficient algo.

## Step 1: Initial Idea &mdash; Row Sets + Neighbor Checks (No IDs, Just Columns)
Thought: Why bother with full grid? Group lands by row into "sets" of column indices. E.g.:
- Row 0: [1,2] (columns with land)
- Row 1: [2,3]
- Row 2: [3]

Path logic: Start from row 0 col, move to row 1:
- Vertical: same col exists in next set? &rarr; Yes, continue.
- Else: Check neighbors (col ±1) in next set &rarr; If yes, move there & continue.

Backtrack if no move. Reach last row &rarr; path exists.

Why this? 
- Small sets per row &rarr; fast existence checks.
- Avoids full grid memory.
- Matches "zig-zag" moves naturally.

Pseudo (my style):
```pseudo
for day from last to first (reverse, add lands backward):
    add cell to its row set
    if all rows have land:
        start from row 0 cols
        dfs(row=0, col=any in set):
            if row == last: return true
            for next_col in row+1 set:
                if next_col == col or abs(next_col - col) == 1:
                    if dfs(row+1, next_col): return true
        if path found: return day
```

Early code snippet (with sets):
```java
// landPerRow[r] = Set of land cols in row r
for (int day = cells.length - 1; day >= 0; day--) {
    int r = cells[day][0] - 1, c = cells[day][1] - 1;
    landPerRow[r].add(c);
    if (all rows non-empty && canReachBottom(0, visited)) return day;
}

private boolean canReachBottom(int r, Set<String> visited) {
    if (r == rowCount) return true;
    for (int col : landPerRow[r]) {
        // skip visited
        visited.add(r + "-" + col);
        if (r + 1 < rowCount) {
            for (int nextCol : landPerRow[r+1]) {
                if (nextCol == col || Math.abs(nextCol - col) == 1) {
                    if (canReachBottom(r+1, visited)) return true;
                }
            }
        }
        visited.remove(r + "-" + col); // backtrack
    }
    return false;
}
```

**Dry run example** (3x3 grid, cells=[[1,2],[2,1],[3,3],[2,2],[1,1],[1,3],[2,3],[3,2],[3,1]]):
- Day 3 (reverse): Sets = Row1:[1,2], Row2:[0,1], Row3:[2]
- Path: (1,2) &rarr; (2,1) [neighbor] &rarr; (3,2) [vertical] &rarr; success.

Pros: Simple mapping, no full grid. Cons: Sets don't enforce *grid* adjacency perfectly (e.g., allows jumps if cols differ by 1 but not truly connected).

## Step 2: Early Issues &mdash; Invalid Paths from Loose Neighbor Checks
Ran into bug: In sets, `abs(nextCol - col) == 1` allows "diagonal-ish" jumps that aren't real grid moves. E.g.:
- Row2: [2], Row3: [0,1]
- From col=2 &rarr; nextCol=1 (abs=1) &rarr; valid? But in grid, (2,2) to (3,1) is diagonal, not allowed!

Why? Sets ignore full grid layout; just checks col diff, not position.

Fix thought: Ditch pure sets for path checks &rarr; use full grid for adjacency, but keep sets for quick "has land" checks.

Transformation:
- Add `boolean[][] land` grid for true adjacency.
- Use sets only for row lands (optional, for printing/debug).
- DFS: Full 4-dir moves on grid: `dirs = {{1,0},{-1,0},{0,1},{0,-1}}`.
- Start DFS from top row grid lands.

Updated pseudo:
```pseudo
for day from last to first:
    land[r][c] = true  // add land (reverse flood)
    if all rows have land:
        visited = new bool[row][col]
        for j in 0 to col-1:
            if land[0][j] and dfs(0, j, visited):
                return day

dfs(r, c, visited):
    if !land[r][c] or visited[r][c]: return false
    visited[r][c] = true
    if r == row-1: return true
    for dir in dirs:
        nr = r + dr, nc = c + dc
        if in bounds and dfs(nr, nc, visited): return true
    visited[r][c] = false  // backtrack
    return false
```

Now paths are grid-correct: No invalid jumps like 2&rarr;0.

Code evolution: From set-only DFS &rarr; hybrid grid + optional sets &rarr; pure grid DFS (faster lookups).

## Step 3: Cleanups &mdash; Remove Prints, Use Sets, Drop Empty Checks
Debug hell: Prints for paths/sets cluttered code. Thought: "Clean it up &mdash; no prints, just logic."

Changes:
- Ditch prints: No `System.out` for paths/sets.
- Use `Set<Integer>[] landPerRow` for row lands (fast contains()).
- Drop `allNonEmpty` loop: DFS fails naturally if a row empty (no lands to reach).

Why? Scanning rows each day = O(row * col) waste. DFS skips empty rows auto.

Updated code snippet (mid-stage):
```java
Set<Integer>[] landPerRow = new HashSet[row];
for (day = last to 0):
    landPerRow[r].add(c)
    visited = new bool[row][col]
    for (j : landPerRow[0]):
        if (dfs(0, j, visited)): return day

dfs(r, c, visited):
    if (!landPerRow[r].contains(c) || visited[r][c]): return false
    // ... same 4-dir DFS
```

Pros: Faster lookups (set contains O(1)), no redundant loops. Cons: Still O(days * row * col) time.

## Step 4: Big Optimization &mdash; From Day-by-Day to Binary Search (Monotonic Magic)
Hit wall: For 40k days, day-by-day DFS = too slow (TLE risk).

Key insight: "Flooding is monotonic &mdash; more days = more water = fewer paths. If cross possible on day X, impossible on X+1? No, wait &mdash; reverse thinking."

Wait, in reverse (adding land back): But forward: More floods &rarr; harder to cross.

Property: Crossing possible days form prefix (1 to some D). Find max D where possible.

Perfect for binary search!

Thought process:
- Naive: Check every day &rarr; O(days * grid).
- Idea: Binary search days &rarr; check log(days) times.
- For mid day: Flood first `mid` cells &rarr; build temp grid &rarr; run same DFS.
- If cross possible &rarr; ans = mid, search later (left = mid+1).
- Else &rarr; search earlier (right = mid-1).

Logic unchanged: Same DFS explores same paths. Just fewer calls.

Pseudo transformation:
```pseudo
Naive loop:
for day = last to 1:
    add land
    if dfs top->bottom: return day

Binary search:
left=1, right=days, ans=0
while left <= right:
    mid = (left+right)/2
    flood first mid cells as water  // temp grid!
    if dfs top->bottom on temp grid:
        ans = mid
        left = mid+1
    else:
        right = mid-1
return ans
```

Why same logic? DFS checks exact same connectivity for that day's grid state. Binary just picks which days to simulate.

Time drop: O(log(days) * row * col) vs O(days * row * col). Huge win!

## Step 5: Final Code &mdash; Binary Search + Grid DFS
Clean, optimized. No sets (grid faster for adjacency), no backtrack (DFS prunes via visited).

```java
import java.util.*;

class Solution {
    int row, col;
    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}}; // down, up, right, left

    public int latestDayToCross(int row, int col, int[][] cells) {
        this.row = row;
        this.col = col;
        int left = 1, right = cells.length;
        int ans = 0;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (canCross(cells, mid)) {
                ans = mid;        // crossing possible
                left = mid + 1;   // try later days
            } else {
                right = mid - 1;  // try earlier days
            }
        }
        return ans;
    }

    private boolean canCross(int[][] cells, int day) {
        boolean[][] flooded = new boolean[row][col];  // true = water
        for (int i = 0; i < day; i++) {
            int r = cells[i][0] - 1;
            int c = cells[i][1] - 1;
            flooded[r][c] = true;
        }

        boolean[][] visited = new boolean[row][col];

        // Start DFS from top row lands
        for (int c = 0; c < col; c++) {
            if (!flooded[0][c] && dfs(0, c, visited, flooded)) {
                return true;
            }
        }
        return false;
    }

    private boolean dfs(int r, int c, boolean[][] visited, boolean[][] flooded) {
        if (r < 0 || r >= row || c < 0 || c >= col || visited[r][c] || flooded[r][c])
            return false;

        if (r == row - 1) return true; // reached bottom

        visited[r][c] = true;

        for (int[] d : dirs) {
            int nr = r + d[0];
            int nc = c + d[1];
            if (dfs(nr, nc, visited, flooded)) return true;
        }

        return false;  // no backtrack needed (visited stays, but new per check)
    }
}
```

Test: For example input, returns 3 -> correct.

## Step 6: Comparison &mdash; Old vs New Code
| Aspect | Reverse-Day DFS (Naive) | Binary Search + DFS (Optimized) |
|--------|--------------------------|---------------------------------|
| Day Loop | For day=last to 0 (linear) | While left<=right (log(days)) |
| Grid Build | Cumulative add land backward | Temp flood per mid (O(mid) but log times) |
| Path Check | DFS from top lands each day | Same DFS, but only log(days) times |
| Time | O(days * row * col) &mdash; slow! | O(log(days) * row * col) &mdash; fast |
| Space | O(row * col) grid | Same, temp per check |
| Logic | Same DFS paths | Identical DFS, just fewer sims |

## Final Thoughts
Started with sets + neighbor hacks &rarr; fixed to grid DFS &rarr; cleaned up &rarr; binary search boom. Logic evolved but core "path exists?" stayed. Now it's submission-ready, TLE resolved.  
Unknowingly the code is fast as well as very less space taking. Space thing was unintended.

## Result
- Runtime: `56ms` : beats `64.47%` -> I thought it might be  around 30% cuz there is DSU
- Memory: `76.24ms` : beats `82.23%` -> Totally unexpected gain

---
Any new ideas and addons are appreciated.
