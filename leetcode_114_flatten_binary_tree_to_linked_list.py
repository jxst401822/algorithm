"""
LeetCode 第114题：二叉树展开为链表

题目描述：
给你二叉树的根结点 root ，请你将它展开为一个单链表：
1. 展开后的单链表应该同样使用 TreeNode ，其中 right 子指针指向链表中下一个结点，而左子指针始终为 null 。
2. 展开后的单链表应该与二叉树 先序遍历 顺序相同。

示例：
输入：root = [1,2,5,3,4,null,6]
输出：[1,null,2,null,3,null,4,null,5,null,6]

输入：root = []
输出：[]

解题思路：
1. 使用后序遍历的方式处理节点
2. 对于每个节点，将其左子树插入到右子树的位置
3. 将原来的右子树接到左子树的最右节点
4. 将左子树置为null

时间复杂度：O(n)
空间复杂度：O(1)
"""

# 定义二叉树节点
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def flatten(self, root: TreeNode) -> None:
        """
        将二叉树展开为链表
        
        Args:
            root: 二叉树根节点
            
        Returns:
            None，直接修改原树结构
        """
        if not root:
            return
        
        # 先处理左右子树
        self.flatten(root.left)
        self.flatten(root.right)
        
        # 如果左子树为空，直接返回
        if not root.left:
            return
        
        # 找到左子树的最右节点
        left_tail = root.left
        while left_tail.right:
            left_tail = left_tail.right
        
        # 将右子树接到左子树的最右节点
        left_tail.right = root.right
        # 将左子树移到右子树位置
        root.right = root.left
        # 将左子树置为null
        root.left = None 