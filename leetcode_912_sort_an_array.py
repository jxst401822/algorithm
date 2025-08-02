"""
LeetCode 第912题：排序数组

题目描述：
给你一个整数数组 nums，请你将该数组升序排列。

示例：
输入：nums = [5,2,3,1]
输出：[1,2,3,5]

输入：nums = [5,1,1,2,0,0]
输出：[0,0,1,1,2,5]

解题思路：
1. 使用快速排序算法
2. 选择基准元素，将数组分为两部分
3. 递归对左右两部分进行排序
4. 合并结果

时间复杂度：O(n log n) 平均情况
空间复杂度：O(log n)
"""

class Solution:
    def sortArray(self, nums: list[int]) -> list[int]:
        """
        对数组进行升序排序
        
        Args:
            nums: 待排序的数组
            
        Returns:
            排序后的数组
        """
        def quick_sort(left, right):
            if left >= right:
                return
            
            # 选择基准元素
            pivot = nums[left]
            i, j = left, right
            
            while i < j:
                # 从右向左找第一个小于基准的元素
                while i < j and nums[j] >= pivot:
                    j -= 1
                # 从左向右找第一个大于基准的元素
                while i < j and nums[i] <= pivot:
                    i += 1
                
                # 交换元素
                if i < j:
                    nums[i], nums[j] = nums[j], nums[i]
            
            # 将基准元素放到正确位置
            nums[left], nums[i] = nums[i], nums[left]
            
            # 递归排序左右两部分
            quick_sort(left, i - 1)
            quick_sort(i + 1, right)
        
        quick_sort(0, len(nums) - 1)
        return nums 