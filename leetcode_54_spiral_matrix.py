"""
LeetCode 第54题：螺旋矩阵

题目描述：
给你一个 m 行 n 列的矩阵 matrix ，请按照 顺时针螺旋顺序 ，返回矩阵中的所有元素。

示例：
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]

输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
输出：[1,2,3,4,8,12,11,10,9,5,6,7]

解题思路：
1. 使用四个边界变量：top, bottom, left, right
2. 按照右、下、左、上的顺序遍历
3. 每完成一个方向后，调整对应的边界
4. 当top > bottom或left > right时停止

时间复杂度：O(m×n)
空间复杂度：O(1)
"""

class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        """
        按顺时针螺旋顺序返回矩阵中的所有元素
        
        Args:
            matrix: 输入的m×n矩阵
            
        Returns:
            按螺旋顺序排列的元素列表
        """
        if not matrix:
            return []
        
        m, n = len(matrix), len(matrix[0])
        result = []
        
        # 定义四个边界
        top, bottom = 0, m - 1
        left, right = 0, n - 1
        
        while top <= bottom and left <= right:
            # 向右遍历
            for j in range(left, right + 1):
                result.append(matrix[top][j])
            top += 1
            
            # 向下遍历
            for i in range(top, bottom + 1):
                result.append(matrix[i][right])
            right -= 1
            
            # 向左遍历
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    result.append(matrix[bottom][j])
                bottom -= 1
            
            # 向上遍历
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    result.append(matrix[i][left])
                left += 1
        
        return result 