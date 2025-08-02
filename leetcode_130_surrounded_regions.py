"""
LeetCode 第130题：被围绕的区域

题目描述：
给你一个 m x n 的矩阵 board ，由若干字符 'X' 和 'O' 组成，捕获所有被围绕的区域。
被围绕的区间不会存在于边界上，换句话说，任何边界上的 'O' 都不会被填充为 'X'。 任何不在边界上，或不与边界上的 'O' 相连的 'O' 最终都会被填充为 'X'。如果两个元素在水平或垂直方向相邻，则称它们是"相连"的。

示例：
输入：board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
输出：[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]

解题思路：
1. 从边界上的'O'开始进行深度优先搜索
2. 将所有与边界相连的'O'标记为特殊字符（如'E'）
3. 遍历整个矩阵，将剩余的'O'改为'X'，将'E'改回'O'

时间复杂度：O(m×n)
空间复杂度：O(m×n)
"""

class Solution:
    def solve(self, board: list[list[str]]) -> None:
        """
        捕获所有被围绕的区域
        
        Args:
            board: 输入的m×n矩阵
            
        Returns:
            None，直接修改原矩阵
        """
        if not board or not board[0]:
            return
        
        m, n = len(board), len(board[0])
        
        def dfs(i, j):
            # 边界检查
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != 'O':
                return
            
            # 标记为'E'表示与边界相连
            board[i][j] = 'E'
            
            # 向四个方向搜索
            dfs(i + 1, j)
            dfs(i - 1, j)
            dfs(i, j + 1)
            dfs(i, j - 1)
        
        # 从边界开始搜索
        for i in range(m):
            dfs(i, 0)  # 左边界
            dfs(i, n - 1)  # 右边界
        
        for j in range(n):
            dfs(0, j)  # 上边界
            dfs(m - 1, j)  # 下边界
        
        # 遍历整个矩阵，修改字符
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O':
                    board[i][j] = 'X'
                elif board[i][j] == 'E':
                    board[i][j] = 'O' 