package com.company;

public class SortMethods {
    //快排
    public static void quicksort(int[] nums,int start,int end){
        if (start>=end){
            return;
        }
        // int mid = (start+end)/2;
        int mid = start + (int)(Math.random() * (end - start)); //随机快排
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



//链表-归并排序 https://leetcode-cn.com/problems/sort-list/
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode sortList(ListNode head) {
        //链表->归并排序
        if(head==null || head.next==null){
            return head;
        }

        //快慢指针 分成两个链表
        ListNode slow=head,fast=head.next;
        while(fast!=null && fast.next!=null){
            slow = slow.next;
            fast = fast.next.next;//快慢指针
        }
        ListNode second = slow.next;
        slow.next = null; //切断
        ListNode first = head;
        //分结束
        
        //first,second->dfs
        first = sortList(first);
        second = sortList(second);

        return merge(first,second);

    }


    public ListNode merge(ListNode head1,ListNode head2){
        ListNode addhead = new ListNode();
        ListNode temp = addhead;
        while(head1!=null && head2!=null){
            if(head1.val<head2.val){
                temp.next = head1;
                head1 = head1.next;
            }
            else{
                temp.next = head2;
                head2 = head2.next;
            }
            temp = temp.next;
        }
        //接尾巴
        temp.next = (head1==null)?head2:head1;

        return addhead.next;
    }
}