"""
LeetCode 第526题：优美的排列

题目描述：
假设有从 1 到 N 的 N 个整数，如果从这 N 个数字中成功构造出一个数组，使得数组的第 i 位 (1 <= i <= N) 满足如下两个条件中的一个，我们就称这个数组为一个优美的排列。条件：
1. 第 i 位的数字能被 i 整除
2. i 能被第 i 位上的数字整除

现在给定一个整数 N，请问可以构造多少个优美的排列？

示例：
输入：N = 2
输出：2
解释：
第 1 个优美的排列是 [1, 2]:
- 第 1 个位置（i=1）上的数字是1，1能被i=1整除
- 第 2 个位置（i=2）上的数字是2，2能被i=2整除

第 2 个优美的排列是 [2, 1]:
- 第 1 个位置（i=1）上的数字是2，i=1能被2整除
- 第 2 个位置（i=2）上的数字是1，i=2能被1整除

解题思路：
1. 使用回溯算法
2. 从位置1开始，尝试放置每个数字
3. 检查当前位置的数字是否满足条件
4. 使用visited数组记录已使用的数字

时间复杂度：O(k)，k是优美排列的数量
空间复杂度：O(n)
"""

class Solution:
    def countArrangement(self, n: int) -> int:
        """
        计算优美排列的数量
        
        Args:
            n: 整数N
            
        Returns:
            优美排列的数量
        """
        def backtrack(pos, used):
            if pos > n:
                return 1
            
            count = 0
            for num in range(1, n + 1):
                if not used[num] and (pos % num == 0 or num % pos == 0):
                    used[num] = True
                    count += backtrack(pos + 1, used)
                    used[num] = False
            
            return count
        
        used = [False] * (n + 1)
        return backtrack(1, used) 