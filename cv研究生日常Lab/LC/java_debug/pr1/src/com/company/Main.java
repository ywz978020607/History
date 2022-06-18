package com.company;

import java.util.*;
import java.lang.reflect.Method;//反射

public class Main {
    public static void func2(ArrayList<Integer> A1) {
        A1.add(100);
        return;
    }

    public static void main(String[] args) {
        // write your code here
        Solution solution = new Solution();

        Scanner sc=new Scanner(System.in);

        while (sc.hasNext()){
            String templine = sc.nextLine();
            if(templine.equals("")){
                continue;
            }

            //非通用部分
            String[] inputStr = templine.split(",");
//            System.out.println(Arrays.toString(inputStr));
            int[] a = new int[inputStr.length];
            //执行leetcode 入口
            for(int ii=0;ii<a.length;ii++){
                a[ii] = Integer.parseInt(inputStr[ii]);
            }
            //获取输出
            int[] b;
            b = solution.constructArr(a);

            //输出
            System.out.println(Arrays.toString(b));
        }

    }
}

//leetcode
class Solution {
    public int[] constructArr(int[] a) {
        int[] b = new int[a.length];
        int temp = 1;
        for(int ii=0;ii<a.length;ii++){
            b[ii] = temp;
            temp *= a[ii];
        }
        temp = 1;
        for(int ii=a.length-1;ii>=0;ii--){
            b[ii] *= temp;
            temp *= a[ii];
        }
        return b;
    }
}