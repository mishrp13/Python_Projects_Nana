class Solution:
    def Pattern3(self,n):
        for i in range(n):
            for j in range(i+1):
                print(i,end= "")
            print()

    def main(self):
        N=5
        sol=Solution()
        sol.Pattern3(N)


if __name__=="__main__":
    Solution().main()
              




