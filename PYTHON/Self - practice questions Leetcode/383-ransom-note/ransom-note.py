class Solution(object):
    def canConstruct(self, ransomNote, magazine):
        """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
        """
        # Initialize an empty dictionary to count elements in magazine
        magazine_count = {}
        
        # Count elements in magazine and store it in the dictionary
        for i in magazine:
            if i in magazine_count:
                magazine_count[i] = magazine_count[i] + 1
            else:
                magazine_count[i] = 1
        
        # Check whether the elements in ransomNote are in magazine
        for i in ransomNote:
            if i in magazine_count and magazine_count[i] > 0:
                magazine_count[i] = magazine_count[i] - 1
            else:
                return False
        
        return True

        
        