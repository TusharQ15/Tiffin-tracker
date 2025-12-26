"""
Problem: Container With Most Water

Source: https://leetcode.com/problems/container-with-most-water/

Difficulty: Medium

Approach:
1. Use two pointers starting from both ends of the array
2. Calculate area between the two pointers and update max area
3. Move the pointer pointing to the shorter line inward
4. Continue until pointers meet

Time Complexity: O(n) - Single pass with two pointers
Space Complexity: O(1) - Constant extra space
"""
from typing import List

def max_area(height: List[int]) -> int:
    """
    Calculate the maximum amount of water a container can store.
    
    Args:
        height: List of non-negative integers representing the height of each line
        
    Returns:
        Maximum area of water that can be contained (integer)
    """
    if len(height) < 2:
        return 0
        
    max_water = 0
    left, right = 0, len(height) - 1
    
    while left < right:
        # Calculate current area
        h = min(height[left], height[right])
        w = right - left
        current_area = h * w
        
        # Update max_water if current area is larger
        max_water = max(max_water, current_area)
        
        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
            
    return max_water


import unittest

class TestMaxArea(unittest.TestCase):
    def test_standard_case(self):
        self.assertEqual(max_area([1,8,6,2,5,4,8,3,7]), 49)
    
    def test_minimum_size(self):
        self.assertEqual(max_area([1, 1]), 1)
        self.assertEqual(max_area([5, 4]), 4)
    
    def test_increasing_heights(self):
        self.assertEqual(max_area([1, 2, 3, 4, 5]), 6)  # 2*3
    
    def test_decreasing_heights(self):
        self.assertEqual(max_area([5, 4, 3, 2, 1]), 6)  # 3*2
    
    def test_tall_edges(self):
        self.assertEqual(max_area([8, 1, 1, 1, 1, 1, 1, 1, 8]), 64)  # 8*8
    
    def test_edge_cases(self):
        self.assertEqual(max_area([]), 0)
        self.assertEqual(max_area([5]), 0)
        self.assertEqual(max_area([0, 0]), 0)
        self.assertEqual(max_area([1, 2, 1]), 2)


if __name__ == "__main__":
    unittest.main()
