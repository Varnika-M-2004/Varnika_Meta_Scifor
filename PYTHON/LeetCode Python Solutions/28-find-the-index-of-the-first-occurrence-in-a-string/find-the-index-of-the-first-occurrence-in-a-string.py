class Solution(object):
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        '''in this we use python's in-built function find() to get the index value of the 
        first occurence of the provided subset of the string from the main string.
        It will return the index value of the first occurence of the subset of the string if it is 
        present in the main string else it'll return -1.
        '''
        index_value = haystack.find(needle)
        return index_value
        
