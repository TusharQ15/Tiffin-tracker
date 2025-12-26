# DSA Patterns and Notes

## Two Pointers Technique
- **When to use**: When dealing with sorted arrays or when you need to find pairs/triplets that satisfy certain conditions.
- **Key Insight**: By using two pointers (one from start, one from end), you can often reduce time complexity from O(n²) to O(n) for certain problems.
- **Example Problems**: Two Sum, Container With Most Water, 3Sum

## Sorting + Two Pointers
- **When to use**: When you need to find combinations (like triplets) that satisfy certain conditions and need to avoid duplicates.
- **Key Insight**: Sorting helps in easily skipping duplicates and enables the two-pointer technique.
- **Example Problems**: 3Sum, 3Sum Closest, 4Sum

## Sliding Window
- **When to use**: When you need to find a subarray or substring that meets certain criteria.
- **Key Insight**: Maintain a window of elements that satisfy the problem constraints and slide it through the array.

## Hash Map/Dictionary
- **When to use**: When you need to store and quickly look up values or their frequencies.
- **Key Insight**: O(1) average time complexity for insertions and lookups.

## Day 5 Notes (2025-03-26)
- **3Sum**: Sorted the array first, then used a combination of iteration and two-pointer technique to find triplets. Key was skipping duplicates to avoid duplicate triplets in the result.
- **Container With Most Water**: Used two pointers starting from both ends, always moving the pointer at the shorter line inward, which ensures we don't miss any potential larger area.
