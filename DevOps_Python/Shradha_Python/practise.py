class Solution:

    def second_largest(self,nums):

        n =len(nums)

        if n <2:
            return -1
        
        largest= float('-inf')
        self.second_largest=float('-inf')

        for i in range(n):
            largest= max(largest, nums[i])

        for i in range(n):
            if nums[i] > self.second_largest and nums[i] != largest:
                self.second_largest=nums[i]

        return -1 if self.second_largest == float('-inf') else self.second_largest
    

nums = [1,2,3,4,56]
sol =Solution()
ans= sol.second_largest(nums)
print("second largest", ans)



       
