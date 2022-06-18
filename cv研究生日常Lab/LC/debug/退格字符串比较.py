#https://leetcode-cn.com/problems/backspace-string-compare/submissions/

class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        iter1=len(s)-1
        iter2=len(t)-1
        while iter1>=0 or iter2>=0:
            if iter1>=0 and iter2>=0 and s[iter1]!="#" and t[iter2]!="#":
                if s[iter1]==t[iter2]:
                    iter1-=1
                    iter2-=1
                else:
                    return False
            elif (iter1>=0 and s[iter1]=="#") or (iter2>=0 and t[iter2]=="#"):
                #若有#
                count1,count2=0,0
                while iter1>=0 and (s[iter1]=="#" or count1>0):
                    if s[iter1]=="#":
                        count1+=1 #还要减一个
                    else:
                        count1-=1
                    iter1-=1 #回到#前一个字符,防止漏掉

                while iter2>=0 and (t[iter2]=="#" or count2>0):
                    if t[iter2]=="#":
                        count2+=1 #还要减一个
                    else:
                        count2-=1
                    iter2-=1 #回到#前一个字符,防止漏掉
            else: #两个有一个小于0，另一个大于等于0且不为#
                return False
        return True

if __name__=="__main__":
    a="hd#dp#czsp#####"
    b="hd#dp#czsp######"
    s=Solution()
    s.backspaceCompare(a,b)
