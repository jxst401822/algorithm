"""
LeetCode 第695题：岛屿的最大面积

题目描述：
给你一个大小为 m x n 的二进制矩阵 grid 。
岛屿 是由一些相邻的 1 (代表土地) 构成的组合，这里的「相邻」要求两个 1 必须在 水平或者竖直的四个方向上 相邻。你可以假设 grid 的四个边缘都被 0（代表水）包围着。
岛屿的面积是岛上值为 1 的单元格的数目。
计算并返回 grid 中最大的岛屿面积。如果没有岛屿，则返回面积为 0 。

示例：
输入：grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
输出：6

解题思路：
1. 使用深度优先搜索（DFS）
2. 遍历整个网格，遇到1时开始DFS
3. 在DFS过程中计算岛屿面积
4. 记录访问过的位置避免重复计算

时间复杂度：O(m×n)
空间复杂度：O(m×n)
"""

class Solution:
    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        """
        计算岛屿的最大面积
        
        Args:
            grid: 二进制矩阵
            
        Returns:
            最大岛屿面积
        """
        if not grid or not grid[0]:
            return 0
        
        m, n = len(grid), len(grid[0])
        max_area = 0
        
        def dfs(i, j):
            # 边界检查或不是陆地
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
                return 0
            
            # 标记为已访问
            grid[i][j] = 0
            area = 1
            
            # 向四个方向搜索
            area += dfs(i + 1, j)
            area += dfs(i - 1, j)
            area += dfs(i, j + 1)
            area += dfs(i, j - 1)
            
            return area
        
        # 遍历整个网格
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    max_area = max(max_area, dfs(i, j))
        
        return max_area 