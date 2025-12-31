// Final solution
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
        boolean[][] land = new boolean[row][col];
        // Mark flooded cells as water
        for (int i = 0; i < day; i++) {
            int r = cells[i][0] - 1;
            int c = cells[i][1] - 1;
            land[r][c] = true; // true = flooded water
        }

        boolean[][] visited = new boolean[row][col];

        // Start DFS/BFS from top row lands
        for (int c = 0; c < col; c++) {
            if (!land[0][c] && dfs(0, c, visited, land)) {
                return true;
            }
        }
        return false;
    }

    private boolean dfs(int r, int c, boolean[][] visited, boolean[][] land) {
        if (r < 0 || r >= row || c < 0 || c >= col || visited[r][c] || land[r][c])
            return false;

        if (r == row - 1) return true; // reached bottom

        visited[r][c] = true;

        for (int[] d : dirs) {
            int nr = r + d[0];
            int nc = c + d[1];
            if (dfs(nr, nc, visited, land)) return true;
        }

        return false;
    }
}
