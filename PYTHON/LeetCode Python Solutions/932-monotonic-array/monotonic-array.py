class Solution(object):
    def isMonotonic(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        '''In this, we use the sorted() in-built python function to first check whether the array is sorted or not.
        If it is not sorted in ascending order, it will use the reverse=True to check whether the array is sorted in the descending order.
        If it satisfies either of the conditions, the function will return True. Else it will return False.
        '''
        if nums == sorted(nums) or nums==sorted(nums, reverse=True):
            return True
        else:
            return False
        
