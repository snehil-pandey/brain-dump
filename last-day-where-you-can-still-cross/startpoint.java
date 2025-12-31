// Main logic building blueprint
class startpoint {
    int rowCount, colCount;
    boolean[][] land;
    int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}}; // down, up, right, left

    public int latestDayToCross(int row, int col, int[][] cells) {
        this.rowCount = row;
        this.colCount = col;
        land = new boolean[row][col];

        // Add land in reverse day order
        for (int day = cells.length - 1; day >= 0; day--) {
            int r = cells[day][0] - 1;
            int c = cells[day][1] - 1;
            land[r][c] = true;

            // Only check if all rows have at least one land
            boolean allNonEmpty = true;
            for (int i = 0; i < row; i++) {
                boolean hasLand = false;
                for (int j = 0; j < col; j++) {
                    if (land[i][j]) {
                        hasLand = true;
                        break;
                    }
                }
                if (!hasLand) {
                    allNonEmpty = false;
                    break;
                }
            }

            if (allNonEmpty) {
                boolean[][] visited = new boolean[row][col];
                for (int j = 0; j < col; j++) {
                    if (land[0][j] && dfs(0, j, visited)) {
                        return day;
                    }
                }
            }
        }

        return -1;
    }

    private boolean dfs(int r, int c, boolean[][] visited) {
        if (!land[r][c] || visited[r][c]) return false;
        visited[r][c] = true;

        if (r == rowCount - 1) return true; // reached bottom

        for (int[] d : dirs) {
            int nr = r + d[0];
            int nc = c + d[1];
            if (nr >= 0 && nr < rowCount && nc >= 0 && nc < colCount) {
                if (dfs(nr, nc, visited)) return true;
            }
        }

        visited[r][c] = false; // backtrack
        return false;
    }
}
