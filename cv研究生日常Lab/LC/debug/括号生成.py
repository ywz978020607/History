class Solution:
    def generateParenthesis(self, n: int):
        #递归回溯
        finalret = []

        def getsub(templist,res_n,res_back):
            # print(templist)

            if res_n==0 and res_back==0:
                if templist not in finalret:
                    finalret.append(templist+")"*res_back)
                return
            else:
                # ( )都要加
                for ii in range(res_n+res_back):
                    if ii<res_n:
                        if ii>0:
                            continue #组合总和II 剪枝方法
                        #加(
                        getsub(templist+"(",res_n-1,res_back+1)
                    else:
                        if ii>res_n: #第一个索引为res_n
                            continue #组合总和II 剪枝方法
                        #加)
                        getsub(templist+")",res_n,res_back-1)
                return templist

        #templist变为字符串
        temp_path = ""
        getsub(temp_path,n,0)
        return finalret


if __name__=="__main__":
    test=Solution()
    res = test.generateParenthesis(7)
    print(res)



