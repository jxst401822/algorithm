"""
LeetCode 第102题：二叉树的层序遍历

题目描述：
给你二叉树的根节点 root ，返回其节点值的 层序遍历 。（即逐层地，从左到右访问所有节点）。

示例：
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]

输入：root = [1]
输出：[[1]]

输入：root = []
输出：[]

解题思路：
1. 使用队列进行广度优先搜索（BFS）
2. 每次处理一层，记录当前层的节点数量
3. 将当前层的所有节点值加入结果列表
4. 将下一层的节点加入队列

时间复杂度：O(n)
空间复杂度：O(n)
"""

# 定义二叉树节点
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque

class Solution:
    def levelOrder(self, root: TreeNode) -> list[list[int]]:
        """
        对二叉树进行层序遍历
        
        Args:
            root: 二叉树根节点
            
        Returns:
            层序遍历结果，每一层作为一个子列表
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            level = []
            
            # 处理当前层的所有节点
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                
                # 将下一层节点加入队列
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level)
        
        return result 