class Solution:

    def Pattern(self,n):
        for i in range(n):
            for j in range(n):
                print("*", end= "")
            print()


    def main(self):
        sol=Solution()
        N=4
        sol.Pattern(N)


if __name__=="__main__":
    Solution().main()




