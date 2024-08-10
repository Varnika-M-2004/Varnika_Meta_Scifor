class Solution(object):
    def moveZeroes(self, nums):
        #store the length of the list in num_len variable
        num_len = len(nums)
        #initialize an empty list to store all non-zero numbers
        non_zero = []
        #iterate through the list
        for i in nums:
            #append all the no-zero numbers in non_zero list
            if i != 0:
                non_zero.append(i)
            else:
                continue

        #find the length of the non-zero list and store it in new_len
        new_len = len(non_zero)
        #find the remaining spaces to insert zeros by subtracting the input list from the newly created non-zero list
        zero_count = num_len - new_len
        #the below line updates the nums list by making sure that all the non-zero numbers are in the beginning of the list.
        nums[:new_len] = non_zero
        #it then fills the remaining spaces by zero
        nums[new_len:] = [0] * zero_count
        
        return nums