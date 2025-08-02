"""
LeetCode 第48题：旋转图像

题目描述：
给定一个 n × n 的二维矩阵表示一个图像，将图像顺时针旋转 90 度。
你必须在原地旋转图像，这意味着你需要直接修改输入的二维矩阵。请不要使用另一个矩阵来旋转图像。

示例：
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[7,4,1],[8,5,2],[9,6,3]]

输入：matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
输出：[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]

解题思路：
1. 先转置矩阵（行列互换）
2. 然后反转每一行
3. 这样就实现了90度顺时针旋转

时间复杂度：O(n²)
空间复杂度：O(1)
"""

class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        """
        将矩阵顺时针旋转90度
        
        Args:
            matrix: 需要旋转的n×n矩阵
            
        Returns:
            None，直接修改原矩阵
        """
        n = len(matrix)
        
        # 转置矩阵
        for i in range(n):
            for j in range(i, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        
        # 反转每一行
        for i in range(n):
            matrix[i].reverse() 