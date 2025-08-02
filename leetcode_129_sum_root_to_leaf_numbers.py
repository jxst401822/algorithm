"""
LeetCode 第129题：求根节点到叶节点数字之和

题目描述：
给你一个二叉树的根节点 root ，树中每个节点都存放有一个 0 到 9 之间的数字。
每条从根节点到叶节点的路径都代表一个数字：
例如，从根节点到叶节点的路径 1 -> 2 -> 3 表示数字 123 。
计算从根节点到叶节点生成的 所有数字之和 。

示例：
输入：root = [1,2,3]
输出：25
解释：
从根到叶子节点路径 1->2 代表数字 12
从根到叶子节点路径 1->3 代表数字 13
因此，数字总和 = 12 + 13 = 25

解题思路：
1. 使用深度优先搜索（DFS）
2. 维护当前路径的数字
3. 当到达叶子节点时，将路径数字加入总和
4. 递归处理左右子树

时间复杂度：O(n)
空间复杂度：O(h)，h为树的高度
"""

# 定义二叉树节点
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sumNumbers(self, root: TreeNode) -> int:
        """
        计算从根节点到叶节点生成的所有数字之和
        
        Args:
            root: 二叉树根节点
            
        Returns:
            所有路径数字之和
        """
        def dfs(node, current_sum):
            if not node:
                return 0
            
            # 更新当前路径的数字
            current_sum = current_sum * 10 + node.val
            
            # 如果是叶子节点，返回当前路径数字
            if not node.left and not node.right:
                return current_sum
            
            # 递归处理左右子树
            return dfs(node.left, current_sum) + dfs(node.right, current_sum)
        
        return dfs(root, 0) 