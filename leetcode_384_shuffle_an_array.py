"""
LeetCode 第384题：打乱数组

题目描述：
给你一个整数数组 nums ，设计算法来打乱一个没有重复元素的数组。实现 Solution class:
- Solution(int[] nums) 使用整数数组 nums 初始化对象
- int[] reset() 重设数组到它的初始状态并返回
- int[] shuffle() 返回数组随机打乱后的结果

示例：
输入：["Solution", "shuffle", "reset", "shuffle"]
[[[1, 2, 3]], [], [], []]
输出：[null, [3, 1, 2], [1, 2, 3], [1, 3, 2]]

解题思路：
1. 保存原始数组的副本
2. reset()方法返回原始数组
3. shuffle()方法使用Fisher-Yates洗牌算法
4. 从后往前遍历，每次随机选择一个位置与当前位置交换

时间复杂度：
- 初始化：O(n)
- reset：O(1)
- shuffle：O(n)
空间复杂度：O(n)
"""

import random

class Solution:
    def __init__(self, nums: list[int]):
        """
        初始化Solution对象
        
        Args:
            nums: 原始数组
        """
        self.original = nums.copy()
        self.nums = nums.copy()
    
    def reset(self) -> list[int]:
        """
        重设数组到初始状态
        
        Returns:
            原始数组
        """
        self.nums = self.original.copy()
        return self.nums
    
    def shuffle(self) -> list[int]:
        """
        返回数组随机打乱后的结果
        
        Returns:
            打乱后的数组
        """
        # Fisher-Yates洗牌算法
        for i in range(len(self.nums) - 1, 0, -1):
            j = random.randint(0, i)
            self.nums[i], self.nums[j] = self.nums[j], self.nums[i]
        
        return self.nums 