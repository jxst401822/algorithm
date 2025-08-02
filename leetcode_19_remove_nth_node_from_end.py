"""
LeetCode 第19题：删除链表的倒数第N个节点

题目描述：
给你一个链表，删除链表的倒数第 n 个节点，并且返回链表的头节点。

示例：
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]

输入：head = [1], n = 1
输出：[]

输入：head = [1,2], n = 1
输出：[1]

解题思路：
1. 使用双指针法（快慢指针）
2. 首先让快指针先走n步
3. 然后快慢指针同时移动，当快指针到达链表末尾时，慢指针指向要删除节点的前一个节点
4. 删除目标节点并返回头节点

时间复杂度：O(L)，其中L是链表的长度
空间复杂度：O(1)
"""

# 定义链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        """
        删除链表的倒数第N个节点
        
        Args:
            head: 链表头节点
            n: 要删除的倒数第n个节点
            
        Returns:
            删除节点后的链表头节点
        """
        # 创建虚拟头节点，简化边界情况处理
        dummy = ListNode(0)
        dummy.next = head
        
        # 初始化快慢指针
        fast = dummy
        slow = dummy
        
        # 快指针先走n步
        for _ in range(n):
            fast = fast.next
        
        # 快慢指针同时移动，直到快指针到达链表末尾
        while fast.next:
            fast = fast.next
            slow = slow.next
        
        # 删除目标节点
        slow.next = slow.next.next
        
        return dummy.next