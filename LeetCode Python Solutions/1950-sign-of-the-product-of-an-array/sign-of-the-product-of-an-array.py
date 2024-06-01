class Solution(object):
    def arraySign(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        mul = 1
        for i in nums:
            mul = i * mul
            i+=1
        return signFunc(mul)

def signFunc(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0





        

        