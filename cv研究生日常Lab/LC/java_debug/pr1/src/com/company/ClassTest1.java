package com.company;

public class ClassTest1 {
    public static <T extends Comparable<T>> T getmax(T x, T y)
    {
        T max = x; // 假设x是初始最大值
        if ( y.compareTo( max ) > 0 ){
            max = y; //y 更大
        }
        return max; // 返回最大对象
    }
}
