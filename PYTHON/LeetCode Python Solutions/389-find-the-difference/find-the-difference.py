class Solution(object):
    def findTheDifference(self, s, t):
        #initialize a dictionary to store character and its count as key-value pairs
        char_count = {}
        #iterating through every character in s
        for i in s:
            #if character is in dictionary, increment count by 1
            if i in char_count:
                char_count[i] += 1
                #if character is not in dictionary, then make the key-value pair and the count of the char as 1
            else:
                char_count[i] = 1
        
        #iterating the t word
        for i in t:
            #if character is not present in the dictionary or is the count of the character is 0 then return character
            if not(i in char_count) or char_count[i]==0:
                return i
                #else, if it is present, then reduce the count by 1 to get the difference.
            else:
                char_count[i] -= 1
           



        