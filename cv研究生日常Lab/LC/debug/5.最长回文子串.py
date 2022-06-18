#动态规划
class Solution:
    def longestPalindrome(self, s: str) -> str:
        # 动态规划
        # d = [[0]*len(s)]*len(s) #!!!!! 错误 不能这么创建

        d = [[0] * len(s) for ii in range(len(s))]  # [[xx]*cols for i in range(rows)]

        maxlen = 1
        laststart = len(s) - 1

        for ii in range(len(s) - 1, -1, -1):
            for jj in range(ii, len(s)):
                # print(d)
                # d[i][j] = d[i+1][j-1] and (s[i]==s[j])
                if ii == jj:
                    d[ii][jj] = 1

                elif s[ii] == s[jj] and (ii==jj-1 or d[ii + 1][jj - 1] == 1):
                    d[ii][jj] = 1

                    if jj - ii + 1 > maxlen:
                        maxlen = jj - ii + 1
                        laststart = ii

        return s[laststart:laststart + maxlen]


if __name__=="__main__":
    test = Solution()
    print(test.longestPalindrome("cbbd"))