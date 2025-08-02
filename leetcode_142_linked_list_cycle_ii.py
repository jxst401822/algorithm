"""
LeetCode 第142题：环形链表II

题目描述：
给定一个链表，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。
为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。

示例：
输入：head = [3,2,0,-4], pos = 1
输出：返回索引为 1 的链表节点

输入：head = [1,2], pos = 0
输出：返回索引为 0 的链表节点

解题思路：
1. 使用快慢指针检测是否有环
2. 如果快慢指针相遇，说明有环
3. 将慢指针重置到头部，快慢指针同时移动
4. 再次相遇的节点就是环的入口

时间复杂度：O(n)
空间复杂度：O(1)
"""

# 定义链表节点
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        """
        检测链表中环的入口节点
        
        Args:
            head: 链表头节点
            
        Returns:
            环的入口节点，如果没有环返回None
        """
        if not head or not head.next:
            return None
        
        # 快慢指针检测环
        slow = fast = head
        
        # 第一次相遇
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return None  # 没有环
        
        # 找到环的入口
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next
        
        return slow 