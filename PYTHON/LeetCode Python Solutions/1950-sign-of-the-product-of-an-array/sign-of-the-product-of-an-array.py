class Solution(object):
    def arraySign(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        #initialize a variable mul to 1
        mul = 1
        #iterate over the numbers and store them in i
        for i in nums:
            #Now, multiply the numbers with each other using the variable mul and i^th number
            mul = i * mul
            #increment value of i
            i+=1
        return signFunc(mul)
#define the signFunc function and pass a number (x) as a parameter
def signFunc(x):
    #in this if the x value is greater than 0 i.e., positive number, return output as 1
    if x > 0:
        return 1
    #in this if the x value is less than 0 i.e., negative number, return output as -1
    elif x < 0:
        return -1
    #else, if number is equal to 0, return 0
    else:
        return 0





        

        
