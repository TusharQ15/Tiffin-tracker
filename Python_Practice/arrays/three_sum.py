"""
Problem: 3Sum

Source: https://leetcode.com/problems/3sum/

Difficulty: Medium

Approach:
1. Sort the array to enable two-pointer technique and skip duplicates
2. For each element, use two pointers to find pairs that sum to -element
3. Skip duplicates to avoid duplicate triplets

Time Complexity: O(n²) - n log n for sorting + n² for two-pointer scan
Space Complexity: O(1) - excluding output storage, O(n) including output
"""
from typing import List

def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Finds all unique triplets in the array which gives the sum of zero.
    
    Args:
        nums: List of integers
        
    Returns:
        List of lists containing unique triplets that sum to zero
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # Skip duplicate elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        left, right = i + 1, n - 1
        target = -nums[i]
        
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
                
    return result


import unittest

class TestThreeSum(unittest.TestCase):
    def test_mixed_positives_negatives(self):
        nums = [-1, 0, 1, 2, -1, -4]
        expected = [[-1, -1, 2], [-1, 0, 1]]
        self.assertEqual(three_sum(nums), expected)
    
    def test_no_solution(self):
        self.assertEqual(three_sum([0, 1, 1]), [])
        self.assertEqual(three_sum([1, 2, -2, -1]), [])
    
    def test_all_zeros(self):
        self.assertEqual(three_sum([0, 0, 0, 0]), [[0, 0, 0]])
    
    def test_duplicates(self):
        nums = [-1, 0, 1, 2, -1, -1, -4]
        expected = [[-1, -1, 2], [-1, 0, 1]]
        self.assertEqual(three_sum(nums), expected)
    
    def test_multiple_triplets(self):
        nums = [-2, 0, 1, 1, 2]
        expected = [[-2, 0, 2], [-2, 1, 1]]
        self.assertEqual(three_sum(nums), expected)
    
    def test_less_than_three_elements(self):
        self.assertEqual(three_sum([]), [])
        self.assertEqual(three_sum([0]), [])
        self.assertEqual(three_sum([1, 2]), [])


if __name__ == "__main__":
    unittest.main()
