class Solution(object):
    def mergeAlternately(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: str
        """
        len1 = len(word1)
        len2 = len(word2)
        total = ""
        i = 0
        j = 0
        while i<len1 and j<len2:
            total += word1[i] + word2[j]
            i+=1
            j+=1
        
        '''if any word is longer than the other, add the remaining characters
        to the end of the final string'''
        total += word1[i:] + word2[j:]
        return total
        
        