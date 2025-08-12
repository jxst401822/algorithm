"""
LeetCode 第146题：LRU缓存机制

题目描述：
请你设计并实现一个满足  LRU (最近最少使用) 缓存 约束的数据结构。
实现 LRUCache 类：
- LRUCache(int capacity) 以 正整数 作为容量 capacity 初始化 LRU 缓存
- int get(int key) 如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1 。
- void put(int key, int value) 如果关键字 key 已经存在，则变更其数据值 value ；如果不存在，则向缓存中插入该组 key-value 。如果插入操作导致关键字数量超过 capacity ，则应该 逐出 最久未使用的关键字。

函数 get 和 put 必须以 O(1) 的平均时间复杂度运行。

示例：
输入：["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
输出：[null, null, null, 1, null, -1, null, -1, 3, 4]

解题思路：
1. 使用哈希表 + 双向链表的数据结构
2. 哈希表提供O(1)的查找能力
3. 双向链表维护访问顺序，最近使用的在头部，最久未使用的在尾部
4. 每次访问或插入时，将节点移动到链表头部
5. 当容量满时，删除链表尾部的节点

时间复杂度：O(1) 所有操作
空间复杂度：O(capacity)
"""

# 定义双向链表节点
class DLinkedNode:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        """
        初始化LRU缓存
        
        Args:
            capacity: 缓存容量
        """
        self.cache = {}  # 哈希表存储key到节点的映射
        self.capacity = capacity
        self.size = 0
        
        # 使用伪头部和伪尾部节点
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key: int) -> int:
        """
        获取缓存中的值
        
        Args:
            key: 要获取的键
            
        Returns:
            对应的值，如果不存在返回-1
        """
        if key not in self.cache:
            return -1
        
        # 如果key存在，先通过哈希表定位，再移到头部
        node = self.cache[key]
        self.moveToHead(node)
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        添加或更新缓存
        
        Args:
            key: 键
            value: 值
        """
        if key not in self.cache:
            # 如果key不存在，创建一个新节点
            node = DLinkedNode(key, value)
            # 添加进哈希表
            self.cache[key] = node
            # 添加至双向链表的头部
            self.addToHead(node)
            self.size += 1
            if self.size > self.capacity:
                # 如果超出容量，删除双向链表的尾部节点
                removed = self.removeTail()
                # 删除哈希表中对应的项
                self.cache.pop(removed.key)
                self.size -= 1
        else:
            # 如果key存在，先通过哈希表定位，再修改value，并移到头部
            node = self.cache[key]
            node.value = value
            self.moveToHead(node)
    
    def addToHead(self, node: DLinkedNode):
        """
        将节点添加到双向链表头部
        
        Args:
            node: 要添加的节点
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def removeNode(self, node: DLinkedNode):
        """
        移除双向链表中的节点
        
        Args:
            node: 要移除的节点
        """
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def moveToHead(self, node: DLinkedNode):
        """
        将节点移动到双向链表头部
        
        Args:
            node: 要移动的节点
        """
        self.removeNode(node)
        self.addToHead(node)
    
    def removeTail(self) -> DLinkedNode:
        """
        移除双向链表尾部节点
        
        Returns:
            被移除的节点
        """
        node = self.tail.prev
        self.removeNode(node)
        return node
