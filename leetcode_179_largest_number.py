"""
LeetCode 第179题：最大数

题目描述：
给定一组非负整数 nums，重新排列每个数的顺序（每个数不可拆分）使之组成一个最大的整数。
注意：输出结果可能非常大，所以你需要返回一个字符串而不是整数。

示例：
输入：nums = [10,2]
输出："210"

输入：nums = [3,30,34,5,9]
输出："9534330"

解题思路：
1. 将数字转换为字符串
2. 自定义排序规则：比较两个字符串拼接后的结果
3. 如果a+b > b+a，则a排在b前面
4. 最后拼接所有字符串

时间复杂度：O(n log n)
空间复杂度：O(n)
"""

from functools import cmp_to_key

class Solution:
    def largestNumber(self, nums: list[int]) -> str:
        """
        重新排列数字组成最大数
        
        Args:
            nums: 非负整数数组
            
        Returns:
            组成最大数的字符串
        """
        # 自定义比较函数
        def compare(a, b):
            if a + b > b + a:
                return -1
            elif a + b < b + a:
                return 1
            else:
                return 0
        
        # 转换为字符串并排序
        str_nums = [str(num) for num in nums]
        str_nums.sort(key=cmp_to_key(compare))
        
        # 拼接结果
        result = ''.join(str_nums)
        
        # 处理全零的情况
        return result if result[0] != '0' else '0' 