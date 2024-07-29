class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        new_word = []
        result = ''
        len_word1 = len(word1)
        len_word2 = len(word2)
        for i in range(max(len_word1, len_word2)):
            if i < len_word1:
                new_word.append(word1[i])
            if i < len_word2:
                new_word.append(word2[i])
        result = ''.join(new_word)
        return result
        