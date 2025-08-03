"""
LeetCode 第678题：有效的括号字符串

题目描述：
给定一个只包含三种字符的字符串：（ ，） 和 *，写一个函数来检验这个字符串是否为有效字符串。有效字符串具有如下规则：
1. 任何左括号 ( 必须有对应的右括号 )。
2. 任何右括号 ) 必须有对应的左括号 ( 。
3. 左括号 ( 必须在对应的右括号 ) 之前。
4. * 可以被视为单个左括号 ( ，或单个右括号 ) ，或一个空字符串。
5. 空字符串也被视为有效字符串。

示例：
输入：s = "()"
输出：true

输入：s = "(*)"
输出：true

输入：s = "(*))"
输出：true

输入：s = "((*)"
输出：true

输入：s = "((*))"
输出：true

输入：s = "(()"
输出：false

解题思路：
1. 使用两个栈分别记录左括号和星号的位置
2. 遍历字符串，遇到左括号和星号时入栈
3. 遇到右括号时，优先匹配左括号，其次匹配星号
4. 最后处理剩余的左括号和星号，确保每个左括号都有对应的星号

时间复杂度：O(n)
空间复杂度：O(n)
"""

class Solution:
    def checkValidString(self, s: str) -> bool:
        """
        检查字符串是否为有效的括号字符串
        
        Args:
            s: 包含括号和星号的字符串
            
        Returns:
            是否为有效字符串
        """
        # 记录左括号和星号的位置
        left_stack = []  # 左括号栈
        star_stack = []  # 星号栈
        
        for i, char in enumerate(s):
            if char == '(':
                left_stack.append(i)
            elif char == '*':
                star_stack.append(i)
            elif char == ')':
                # 优先匹配左括号
                if left_stack:
                    left_stack.pop()
                # 其次匹配星号
                elif star_stack:
                    star_stack.pop()
                else:
                    # 没有可匹配的，返回False
                    return False
        
        # 处理剩余的左括号，需要星号来匹配
        while left_stack and star_stack:
            # 确保星号在左括号之后
            if left_stack[-1] < star_stack[-1]:
                left_stack.pop()
                star_stack.pop()
            else:
                break
        
        # 如果还有左括号没有匹配，返回False
        return len(left_stack) == 0
    
    def checkValidString_alternative(self, s: str) -> bool:
        """
        另一种解法：使用贪心算法
        维护未匹配的左括号的最小值和最大值
        
        Args:
            s: 包含括号和星号的字符串
            
        Returns:
            是否为有效字符串
        """
        min_left = 0  # 未匹配左括号的最小值
        max_left = 0  # 未匹配左括号的最大值
        
        for char in s:
            if char == '(':
                min_left += 1
                max_left += 1
            elif char == ')':
                min_left = max(0, min_left - 1)
                max_left -= 1
                if max_left < 0:
                    return False
            elif char == '*':
                min_left = max(0, min_left - 1)
                max_left += 1
        
        return min_left == 0 