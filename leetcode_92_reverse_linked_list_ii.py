"""
LeetCode 第92题：反转链表II

题目描述：
给你单链表的头指针 head 和两个整数 left 和 right ，其中 left <= right 。请你反转从位置 left 到位置 right 的链表节点，返回 反转后的链表 。

示例：
输入：head = [1,2,3,4,5], left = 2, right = 4
输出：[1,4,3,2,5]

输入：head = [5], left = 1, right = 1
输出：[5]

解题思路：
1. 使用虚拟头节点简化边界情况处理
2. 找到left位置的前一个节点
3. 使用头插法反转从left到right的节点
4. 连接反转后的链表

时间复杂度：O(n)
空间复杂度：O(1)
"""

# 定义链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseBetween(self, head: ListNode, left: int, right: int) -> ListNode:
        """
        反转链表中从位置left到位置right的节点
        
        Args:
            head: 链表头节点
            left: 反转起始位置（从1开始）
            right: 反转结束位置
            
        Returns:
            反转后的链表头节点
        """
        # 创建虚拟头节点
        dummy = ListNode(0)
        dummy.next = head
        
        # 找到left位置的前一个节点
        prev = dummy
        for _ in range(left - 1):
            prev = prev.next
        
        # 开始反转
        curr = prev.next
        for _ in range(right - left):
            next_node = curr.next
            curr.next = next_node.next
            next_node.next = prev.next
            prev.next = next_node
        
        return dummy.next 