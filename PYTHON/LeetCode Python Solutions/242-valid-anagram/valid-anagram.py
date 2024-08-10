class Solution(object):
    def isAnagram(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        '''in this we use the python in-built function called sorted(). It will check whether the characters are same in 
        both the words irrespective of their arrangement. If yes, then it will return true, else will return false
        '''
        if sorted(s) == sorted(t):
            return True
        else:
            return False
        
