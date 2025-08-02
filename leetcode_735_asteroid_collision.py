"""
LeetCode 第735题：行星碰撞

题目描述：
给定一个整数数组 asteroids，表示在同一行的行星。
对于数组中的每一个元素，其绝对值表示行星的大小，正负表示行星的移动方向（正表示向右移动，负表示向左移动）。如果两颗行星相遇，则较小的行星会爆炸。如果两颗行星大小相同，则两颗行星都会爆炸。两颗移动方向相反的行星才会发生碰撞。

示例：
输入：asteroids = [5,10,-5]
输出：[5,10]
解释：10 和 -5 碰撞后只剩下 10 。 5 和 10 永远不会发生碰撞。

输入：asteroids = [8,-8]
输出：[]
解释：8 和 -8 碰撞后，两者都发生爆炸。

解题思路：
1. 使用栈来模拟碰撞过程
2. 遍历数组，对于每个行星：
   - 如果栈为空或当前行星向右移动，直接入栈
   - 如果当前行星向左移动，与栈顶行星比较
   - 根据大小关系决定是否爆炸

时间复杂度：O(n)
空间复杂度：O(n)
"""

class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        """
        模拟行星碰撞过程
        
        Args:
            asteroids: 行星数组
            
        Returns:
            碰撞后的行星数组
        """
        stack = []
        
        for asteroid in asteroids:
            # 当前行星向左移动且栈不为空
            while stack and asteroid < 0 and stack[-1] > 0:
                # 比较大小
                if abs(asteroid) > stack[-1]:
                    stack.pop()  # 栈顶行星爆炸
                elif abs(asteroid) == stack[-1]:
                    stack.pop()  # 两者都爆炸
                    break
                else:
                    # 当前行星爆炸
                    break
            else:
                # 没有发生碰撞，入栈
                stack.append(asteroid)
        
        return stack 