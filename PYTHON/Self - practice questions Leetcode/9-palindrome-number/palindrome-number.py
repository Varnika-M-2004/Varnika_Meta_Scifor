class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        while x >= 0:
            #convert integer to string and check if it is equal
            str_x = str(x)
            return str_x == str_x[::-1]
        