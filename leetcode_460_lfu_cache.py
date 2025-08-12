"""
LeetCode 第460题：LFU缓存

题目描述：
请你为 最不经常使用（LFU）缓存算法设计并实现数据结构。

实现 LFUCache 类：
- LFUCache(int capacity) - 用数据结构的容量 capacity 初始化对象
- int get(int key) - 如果键 key 存在于缓存中，则获取键的值，否则返回 -1 。
- void put(int key, int value) - 如果键 key 已存在，则变更其值；如果键不存在，请插入键值对。当缓存达到其容量 capacity 时，则应该在插入新项之前，使最不经常使用的项无效。在此问题中，当存在平局（即两个或更多个键具有相同使用频率）时，应该去除 最近最久未使用 的键。

为了确定最不经常使用的键，可以为缓存中的每个键维护一个 使用计数器 。使用计数最小的键是最久未使用的键。

当一个键首次插入到缓存中时，它的使用计数器被设置为 1 (由于 put 操作)。对缓存中的键执行 get 或 put 操作，使用计数器的值将会递增。

函数 get 和 put 必须以 O(1) 的平均时间复杂度运行。

示例：
输入：["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
输出：[null, null, null, 1, null, -1, 3, null, -1, 3, 4]

解题思路：
1. 使用哈希表 + 双向链表的数据结构
2. 哈希表存储key到节点的映射
3. 使用频率哈希表存储频率到双向链表的映射
4. 每个频率对应一个双向链表，维护该频率下的所有节点
5. 记录最小频率，用于快速找到要删除的节点
6. 使用伪头部和伪尾部节点简化链表操作

时间复杂度：O(1) 所有操作
空间复杂度：O(capacity)
"""

# 定义双向链表节点
class DLinkedNode:
    def __init__(self, key=0, value=0, freq=0):
        self.key = key
        self.value = value
        self.freq = freq
        self.prev = None
        self.next = None

# 定义双向链表
class DLinkedList:
    def __init__(self):
        self.head = DLinkedNode()  # 伪头部
        self.tail = DLinkedNode()  # 伪尾部
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0
    
    def addToHead(self, node: DLinkedNode):
        """将节点添加到链表头部"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1
    
    def removeNode(self, node: DLinkedNode):
        """移除链表中的节点"""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
    
    def removeTail(self) -> DLinkedNode:
        """移除链表尾部节点"""
        node = self.tail.prev
        self.removeNode(node)
        return node

class LFUCache:
    def __init__(self, capacity: int):
        """
        初始化LFU缓存
        
        Args:
            capacity: 缓存容量
        """
        self.capacity = capacity
        self.size = 0
        self.minFreq = 0
        
        # 存储key到节点的映射
        self.keyTable = {}
        # 存储频率到双向链表的映射
        self.freqTable = {}
    
    def get(self, key: int) -> int:
        """
        获取缓存中的值
        
        Args:
            key: 要获取的键
            
        Returns:
            对应的值，如果不存在返回-1
        """
        if key not in self.keyTable:
            return -1
        
        # 获取节点并更新频率
        node = self.keyTable[key]
        self.updateFreq(node)
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        添加或更新缓存
        
        Args:
            key: 键
            value: 值
        """
        if self.capacity == 0:
            return
        
        if key not in self.keyTable:
            # 如果key不存在，创建新节点
            node = DLinkedNode(key, value, 1)
            self.keyTable[key] = node
            
            # 如果容量已满，删除最不经常使用的节点
            if self.size >= self.capacity:
                self.removeLeastFreqNode()
            else:
                self.size += 1
            
            # 将节点添加到频率为1的链表中
            if 1 not in self.freqTable:
                self.freqTable[1] = DLinkedList()
            self.freqTable[1].addToHead(node)
            self.minFreq = 1
        else:
            # 如果key存在，更新值并更新频率
            node = self.keyTable[key]
            node.value = value
            self.updateFreq(node)
    
    def updateFreq(self, node: DLinkedNode):
        """
        更新节点的使用频率
        
        Args:
            node: 要更新的节点
        """
        freq = node.freq
        # 从当前频率的链表中移除
        self.freqTable[freq].removeNode(node)
        
        # 如果当前频率的链表为空，删除该频率
        if self.freqTable[freq].size == 0:
            del self.freqTable[freq]
            # 如果删除的是最小频率，更新最小频率
            if freq == self.minFreq:
                self.minFreq += 1
        
        # 增加频率
        node.freq += 1
        freq = node.freq
        
        # 添加到新频率的链表中
        if freq not in self.freqTable:
            self.freqTable[freq] = DLinkedList()
        self.freqTable[freq].addToHead(node)
    
    def removeLeastFreqNode(self):
        """移除最不经常使用的节点"""
        # 从最小频率的链表中移除尾部节点
        node = self.freqTable[self.minFreq].removeTail()
        
        # 如果该频率的链表为空，删除该频率
        if self.freqTable[self.minFreq].size == 0:
            del self.freqTable[self.minFreq]
        
        # 从key表中删除
        del self.keyTable[node.key]
