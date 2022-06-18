# 快速排序
import random

def quicksort(list):
    # 挑选一个归拢两边
    def partition(list,begin,end):
        if begin>=end:
            return
        select_index = random.randint(begin,end)
        select_val = list[select_index]
        #左右互换
        list[select_index],list[end] = list[end],list[select_index]

        temp_iter = begin #递进指针
        for ii in range(begin,end):
            if list[ii]<select_val:
                #与左递进指针交换
                list[temp_iter],list[ii] = list[ii],list[temp_iter]
                temp_iter += 1

        # 左右互换回来
        list[temp_iter], list[end] = list[end], list[temp_iter]

        #递归
        partition(list,begin,temp_iter-1)
        partition(list,temp_iter+1,end)
    ###
    partition(list,0,len(list)-1) #数组是引用调用，直接修改即可


# 数组--堆排序
def heapsort(arr):
    def heapadjust(arr,start,end): #[start,end)
        #最大堆维护--从顶向下进行
        while start is not None and start<end//2: #只有当是子节点时start=end//2 （end输入的是len(A)一类的+1值）
            #数组--获取左右子节点
            left,right = start*2+1,start*2+2 #注意此处right可能会等于end，这种情况下面要排除
            swap = None #待交换
            if arr[left]>arr[start]:
                swap = left
            if right<end and arr[right]>arr[start] and (swap==None or arr[right]>arr[left]):
                #充分考虑到end//2对应多值性导致right可能会越界、父和左右子节点选最大原则
                swap = right

            if swap!=None:
                arr[swap],arr[start] = arr[start],arr[swap]
            #下一次父节点换成替换过的节点，若未替换则变成None
            start=swap
    ###
    #堆排序
    #1.构造最大堆n/2次
    for ii in range(len(arr)//2 - 1,-1,-1): #注意这三个-1 特别是第一个
        heapadjust(arr,start=ii,end=len(arr))
    #2.不断取出堆顶、重新构造
    for ii in range(len(arr)-1,0,-1):
        arr[0],arr[ii] = arr[ii],arr[0]
        heapadjust(arr,start=0,end=ii)
    # return A

if __name__ == "__main__":
    list = [3,5,7,2,4,1,4,7,8,9,13]

    # quicksort(list) #数组 索引  修改值会自动变
    heapsort(list)
    print(list)
