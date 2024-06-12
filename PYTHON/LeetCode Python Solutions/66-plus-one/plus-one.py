class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        # Find the length of the digits
        len_digits = len(digits)
        # Iterate from the last digit to the first digit (the first digit's index will be -1) with a step of -1 as we're traversing in a reverse order
        for i in range(len_digits - 1, -1, -1):
            # If digit value is equal to 9 then replace by 0
            if digits[i] == 9:
                digits[i] = 0
            # Else increment value by 1
            else:
                digits[i] += 1
                break

        # If all digits are 9, then all values will be replaced by 0, therefore just insert 1 at the beginning
        if digits[0] == 0:
            digits.insert(0, 1)
        return digits
