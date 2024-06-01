class Solution(object):
    def mergeAlternately(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: str
        """
        #check the length of the words and store them in variables
        len1 = len(word1)
        len2 = len(word2)
        #initialize a variable total to save the final word
        total = ""
        #alsi initialize variables i and j, both of which will iterate over word1 and word2 resp.
        i = 0
        j = 0
        #while we don't reach the end of the strings we will iterate
        while i<len1 and j<len2:
            #in this the total variable will store the alternate words from word1 and word2
            total += word1[i] + word2[j]
            #increment values of i and j by 1
            i+=1
            j+=1
        
        #check if any word is longer than the other, and add the left out words to the end of the final word 'total''''
        total += word1[i:] + word2[j:]
        return total
        
        
