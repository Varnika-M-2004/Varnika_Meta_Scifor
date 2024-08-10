class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        max_value=len(nums)//2
        #initialize an empty dictionary to store count of each element
        value_count = {}
        for i in nums:
            if i in value_count:
                value_count[i] = value_count[i] + 1
            else:
                value_count[i] = 1
            if value_count[i] > max_value:
                return i
        