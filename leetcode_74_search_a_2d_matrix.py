"""
LeetCode 第74题：搜索二维矩阵

题目描述：
编写一个高效的算法来判断 m x n 矩阵中，是否存在一个目标值。该矩阵具有如下特性：
1. 每行中的整数从左到右按非递减顺序排列。
2. 每行的第一个整数大于前一行的最后一个整数。

示例：
输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
输出：true

输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
输出：false

解题思路：
1. 将二维矩阵视为一维有序数组
2. 使用二分查找算法
3. 通过行列转换公式将一维索引转换为二维坐标

时间复杂度：O(log(m×n))
空间复杂度：O(1)
"""

class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        """
        在二维矩阵中搜索目标值
        
        Args:
            matrix: 输入的m×n矩阵
            target: 要搜索的目标值
            
        Returns:
            如果目标值存在于矩阵中返回True，否则返回False
        """
        if not matrix or not matrix[0]:
            return False
        
        m, n = len(matrix), len(matrix[0])
        left, right = 0, m * n - 1
        
        while left <= right:
            mid = (left + right) // 2
            # 将一维索引转换为二维坐标
            row, col = mid // n, mid % n
            value = matrix[row][col]
            
            if value == target:
                return True
            elif value < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return False 