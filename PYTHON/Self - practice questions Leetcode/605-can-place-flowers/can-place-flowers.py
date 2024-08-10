class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        len_bed = len(flowerbed)
        count = 0  # To count how many flowers we can place
        i = 0
        while i < len_bed:
            if flowerbed[i]==0:
                prev_empty = (i==0) or (flowerbed[i-1]==0)
                next_empty = (i==len_bed-1) or (flowerbed[i+1]==0)

                if prev_empty and next_empty:
                    flowerbed[i]==1
                    count+=1
                    # Skip the next spot to avoid placing adjacent flowers
                    i+=1

                    if n==0:
                        return True
            # Move to the next position
            i += 1
            
        return count>=n
        