"""
LeetCode 第622题：设计循环队列

题目描述：
设计你的循环队列实现。 循环队列是一种线性数据结构，其操作表现基于 FIFO（先进先出）原则并且队尾被连接在队首之后以形成一个循环。它也被称为"环形缓冲器"。

实现 MyCircularQueue 类：
- MyCircularQueue(k): 构造器，设置队列长度为 k 。
- Front: 从队首获取元素。如果队列为空，返回 -1 。
- Rear: 获取队尾元素。如果队列为空，返回 -1 。
- enQueue(value): 向循环队列插入一个元素。如果成功插入则返回真。
- deQueue(): 从循环队列中删除一个元素。如果成功删除则返回真。
- isEmpty(): 检查循环队列是否为空。
- isFull(): 检查循环队列是否已满。

解题思路：
1. 使用数组实现循环队列
2. 使用front和rear指针
3. 使用size变量记录当前元素个数
4. 注意边界条件的处理

时间复杂度：O(1) 所有操作
空间复杂度：O(k)
"""

class MyCircularQueue:
    def __init__(self, k: int):
        """
        初始化循环队列
        
        Args:
            k: 队列长度
        """
        self.queue = [0] * k
        self.front = 0
        self.rear = 0
        self.size = 0
        self.capacity = k
    
    def enQueue(self, value: int) -> bool:
        """
        向循环队列插入一个元素
        
        Args:
            value: 要插入的值
            
        Returns:
            是否成功插入
        """
        if self.isFull():
            return False
        
        self.queue[self.rear] = value
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
        return True
    
    def deQueue(self) -> bool:
        """
        从循环队列中删除一个元素
        
        Returns:
            是否成功删除
        """
        if self.isEmpty():
            return False
        
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True
    
    def Front(self) -> int:
        """
        从队首获取元素
        
        Returns:
            队首元素，如果队列为空返回-1
        """
        if self.isEmpty():
            return -1
        return self.queue[self.front]
    
    def Rear(self) -> int:
        """
        获取队尾元素
        
        Returns:
            队尾元素，如果队列为空返回-1
        """
        if self.isEmpty():
            return -1
        return self.queue[(self.rear - 1) % self.capacity]
    
    def isEmpty(self) -> bool:
        """
        检查循环队列是否为空
        
        Returns:
            是否为空
        """
        return self.size == 0
    
    def isFull(self) -> bool:
        """
        检查循环队列是否已满
        
        Returns:
            是否已满
        """
        return self.size == self.capacity 