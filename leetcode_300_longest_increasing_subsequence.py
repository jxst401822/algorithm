"""
LeetCode 第300题：最长递增子序列

题目描述：
给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。
子序列是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子序列。

示例：
输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。

输入：nums = [0,1,0,3,2,3]
输出：4

解题思路：
1. 使用动态规划
2. dp[i]表示以nums[i]结尾的最长递增子序列长度
3. 对于每个位置i，遍历前面的所有位置j
4. 如果nums[i] > nums[j]，则dp[i] = max(dp[i], dp[j] + 1)

时间复杂度：O(n²)
空间复杂度：O(n)
"""

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        """
        计算最长递增子序列的长度
        
        Args:
            nums: 整数数组
            
        Returns:
            最长递增子序列的长度
        """
        if not nums:
            return 0
        
        n = len(nums)
        dp = [1] * n
        
        for i in range(1, n):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
        
        return max(dp) 