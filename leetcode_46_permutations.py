"""
LeetCode 第46题：全排列

题目描述：
给定一个不含重复数字的数组 nums，返回其所有可能的全排列。你可以按任意顺序返回答案。

示例：
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

输入：nums = [0,1]
输出：[[0,1],[1,0]]

输入：nums = [1]
输出：[[1]]

解题思路：
1. 使用回溯算法（Backtracking）
2. 通过交换元素的方式生成所有可能的排列
3. 使用递归来构建排列树
4. 当路径长度等于数组长度时，将当前排列加入结果集

时间复杂度：O(n!)，其中n是数组的长度
空间复杂度：O(n)，递归调用栈的深度
"""

class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        """
        生成数组的全排列
        
        Args:
            nums: 输入数组，不包含重复数字
            
        Returns:
            所有可能的全排列列表
        """
        def backtrack(start: int):
            # 如果起始位置到达数组末尾，说明找到一个排列
            if start == len(nums):
                result.append(nums[:])  # 使用切片创建副本
                return
            
            # 从起始位置开始，依次与后面的元素交换
            for i in range(start, len(nums)):
                # 交换元素
                nums[start], nums[i] = nums[i], nums[start]
                
                # 递归处理下一个位置
                backtrack(start + 1)
                
                # 回溯：恢复交换
                nums[start], nums[i] = nums[i], nums[start]
        
        result = []
        backtrack(0)
        return result
    
    def permute_alternative(self, nums: list[int]) -> list[list[int]]:
        """
        另一种实现方式：使用used数组标记已使用的元素
        
        Args:
            nums: 输入数组，不包含重复数字
            
        Returns:
            所有可能的全排列列表
        """
        def backtrack(path: list[int], used: list[bool]):
            # 如果路径长度等于数组长度，找到一个排列
            if len(path) == len(nums):
                result.append(path[:])
                return
            
            # 遍历所有元素
            for i in range(len(nums)):
                # 如果元素未被使用
                if not used[i]:
                    # 标记为已使用
                    used[i] = True
                    path.append(nums[i])
                    
                    # 递归处理下一个位置
                    backtrack(path, used)
                    
                    # 回溯：恢复状态
                    path.pop()
                    used[i] = False
        
        result = []
        used = [False] * len(nums)
        backtrack([], used)
        return result


# 测试代码
def test_permute():
    """测试全排列算法"""
    solution = Solution()
    
    # 测试用例1
    nums1 = [1, 2, 3]
    result1 = solution.permute(nums1)
    print(f"输入：{nums1}")
    print(f"输出：{result1}")
    print(f"排列数量：{len(result1)}")
    print()
    
    # 测试用例2
    nums2 = [0, 1]
    result2 = solution.permute(nums2)
    print(f"输入：{nums2}")
    print(f"输出：{result2}")
    print(f"排列数量：{len(result2)}")
    print()
    
    # 测试用例3
    nums3 = [1]
    result3 = solution.permute(nums3)
    print(f"输入：{nums3}")
    print(f"输出：{result3}")
    print(f"排列数量：{len(result3)}")
    print()
    
    # 测试用例4
    nums4 = [1, 2, 3, 4]
    result4 = solution.permute(nums4)
    print(f"输入：{nums4}")
    print(f"输出：{result4}")
    print(f"排列数量：{len(result4)}")
    print(f"预期排列数量：{4!}")  # 4! = 24


if __name__ == "__main__":
    test_permute() 