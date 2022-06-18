package com.company;

public class SortMethods {
    //快排
    public static void quicksort(int[] nums,int start,int end){
        if (start>=end){
            return;
        }
        int mid = (start+end)/2;
        int sel_val = nums[mid];
        nums[mid] = nums[end];
        nums[end] = sel_val;
        int temp_left = start;

        for(int ii=start;ii<end;ii++){
            if (nums[ii]<sel_val){ //大于号 降序  小于号 升序
                int temp = nums[ii];
                nums[ii] = nums[temp_left];
                nums[temp_left] = temp;
                temp_left++;
            }
        }
        int temp = nums[end];
        nums[end] = nums[temp_left];
        nums[temp_left] = temp;

        quicksort(nums,start,temp_left-1);
        quicksort(nums,temp_left+1,end);
    }

    //堆排序 --构造最大堆-结果为升序排序
    public static void heapadjust(int[] nums,int start,int end){
        //最大堆维护 从顶向下
        while (start!=-1 && start*2<end){
            int left=start*2+1,right=start*2+2; //真实索引
            int swap = -1;
            //左右交换最大的  同时考虑right可能越界
            if(nums[left]>nums[start]){
                swap = left;
            }
            //再判断右节点
            if(right<=end && nums[right]>nums[start] && (swap==-1 || nums[right]>nums[left])){
                swap = right;
            }
            //只swap一次
            if (swap!=-1){
                int temp = nums[swap];
                nums[swap] = nums[start];
                nums[start] = temp;
            }

            start = swap;
        }
    }
    public static void heapsort(int[] nums,int start,int end){
        //每个父节点都构造一个堆--倒序构造
        for(int ii=end/2;ii>=0;ii--){
            heapadjust(nums,ii,end);
        }

        //堆顶放尾部 再调整
        for(int ii=end;ii>=0;ii--){
            int temp = nums[0];
            nums[0] = nums[ii];
            nums[ii] = temp;

            heapadjust(nums,start,ii-1);
        }
    }
}
