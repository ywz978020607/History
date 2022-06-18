###### 常用算法-排序、最小优先队列(堆维护)

[502. IPO - 力扣（LeetCode） (leetcode-cn.com)](https://leetcode-cn.com/problems/ipo/)

```java
int[][] projects = new int[profits.length][2]; //自定义结构 二维数组
//排序投资成本 a-b是默认升序  但注意如果是一维int[] 只能默认升序！
Arrays.sort(projects,(a,b)->a[0]-b[0]); //升序--默认  使用Arrays.sort() 修改排序标准因为是二维int数组或是类才可以，一维数组原始数据类型int不可以

//优先队列 b-a是降序--最大优先
PriorityQueue<Integer> cur = new PriorityQueue<>( (a,b)->b-a );//改成降序-最大堆
.add() .offer()  .poll() .peek()
//自定义的另一种复杂写法--定义Comparator
PriorityQueue<int[]> pq = new PriorityQueue<int[]>(new Comparator<int[]>() {
    public int compare(int[] pair1, int[] pair2) {
        return pair1[0] != pair2[0] ? pair2[0] - pair1[0] : pair2[1] - pair1[1];
    }
});
//or simply version.
PriorityQueue<Integer> cur = new PriorityQueue<>( (a,b)->b[0]-a[0] );//改成降序-最大堆
链接：https://leetcode-cn.com/problems/hua-dong-chuang-kou-de-zui-da-zhi-lcof/solution/hua-dong-chuang-kou-de-zui-da-zhi-by-lee-ymyo/

//遍历优先队列-迭代器
//使用iterator()方法
Iterator<Integer> iterate = numbers.iterator();
while(iterate.hasNext()) {
    System.out.print(iterate.next());
    System.out.print(", ");
}
```

###### Arrays.sort-实现基本类型降序排序-自定义Comparator

```java
import java.util.Arrays;
import java.util.Comparator;
public class ArraysSortReverse {
 
	public static void main(String[] args) {
		Integer[] nums = {12,33,5,-9,233,2299,-987,2,0,1,8};
		//利用Arrays.sort() 逆序排列nums,
		//注: 要逆序排列的数组，不能使用基本数据类型，必须使用基本类型对应的类  
		
		//任何可以排序的对象，包括基本类型对应的类（Integer,Double,Character,Byte等）
		//都实现了内部比较器接口comparable。	
		
		//正序排
		Arrays.sort(nums);
		for(int i : nums) {
			System.out.print(i+"\t");
		}
		
		//利用外部比较器逆序排序
		MyCompare mc = new MyCompare();
		Arrays.sort(nums,mc);
		
		System.out.println();
		for(int i : nums) {
			System.out.print(i+"\t");
		}
	}
}
//外部比较器
class MyCompare implements Comparator<Integer>{
 
	@Override
	public int compare(Integer o1, Integer o2) {
		// TODO Auto-generated method stub
		return o1 > o2 ? -1 :(o1==o2 ? 0 :1);
	}
 	 
}
```

###### 无符号右移 

java中使用`>>>1`  c++中用unsigned int

###### Random

```
// java.lang.Math.Random，java.lang包下的所有类都是默认加载的，不需要import
Math.random()  返回double[0,1)
(int)(start + Math.random()*length); // [start, start + length)
```
或
```
// java.util.Random
Random rand = new Random(25); //25是种子，随便给
rand.nextInt(); //Int型随机
rand.nextInt(100); //[0,100)
rand.nextBoolean();
rand.nextDouble(); //[0,1)
rand.nextFloat(); //[0,1)
rand.nextLong(); //Long型随机
```
###### 调试手段 -- playground

 [未命名 - LeetCode Playground (leetcode-cn.com)](https://leetcode-cn.com/playground/NkvhUsKX/)

```java
//打印int[]数组
int[] a1 = {3,4,5};
System.out.println(a1);
System.out.println(Arrays.toString(a1));//打印int数组/String[]

// List<Integer> 转 Integer[]
Integer[] integers2 = list1.toArray(new Integer[0]);
//  调用toArray。传入参数T[] a。这种用法是目前推荐的。
// List<String>转String[]也同理。
//leetcode二维技巧 List<int[]> -> int[][]
vec.toArray(new int[vec.size()][]); //二维数组 -> int[][] leetcode常用！ but 一维用不了！
//原因 ： 必须是泛型String[]的一维可以用 但int是基本类型，用不了一维
```

###### Arrays

```java
Arrays.sort(int[])
Arrays.sort(int[][],(a,b)->a[0]-b[0])
Arrays.fill(int[],int val)

//几个数字转List
Arrays.asList(1,2,3,4);

//List 排序
Collections.sort(list); 
```

###### HashMap

```java
.containsKey()  .containsValue()
for(Integer ii:map1.keySet())
for(Integer ii:map1.values()) //注意！
.getOrDefault(xx,-1);
.put(key,value);  //返回旧的value或null
.remove(key); //返回value
.remove(key,value); //返回true/false
//Entry遍历 -- 7种遍历方式
//https://mp.weixin.qq.com/s/zQBN3UvJDhRTKP6SzcZFKw
// 遍历
Iterator<Map.Entry<Integer, String>> iterator = map.entrySet().iterator();
while (iterator.hasNext()) {
    Map.Entry<Integer, String> entry = iterator.next();
    System.out.println(entry.getKey());
    System.out.println(entry.getValue());
}
// 遍历--常用
for (Map.Entry<Integer, String> entry : map.entrySet()) {
    System.out.println(entry.getKey());
    System.out.println(entry.getValue());
}

//TreeMap高级用法 --默认key升序  而HashMap，HashTable无序
//寻找key>val 或者value>val
TreeMap<Integer, Integer> intervals = new TreeMap<>(new Comparator<Integer>(){
             /* 
             * int compare(Object o1, Object o2) 返回一个基本类型的整型， 
             * 返回负数表示：o1 小于o2， 
             * 返回0 表示：o1和o2相等， 
             * 返回正数表示：o1大于o2。 
             */  
            public int compare(Integer a,Integer b){
                return b-a;            
            }
            });
// 找到 l1 最小的且满足 l1 > val 的区间 interval1 = [l1, r1]
// 如果不存在这样的区间，interval1 为尾迭代器
Map.Entry<Integer, Integer> interval1 = intervals.ceilingEntry(val + 1);
// 找到 l0 最大的且满足 l0 <= val 的区间 interval0 = [l0, r0]
// 在有序集合中，interval0 就是 interval1 的前一个区间
// 如果不存在这样的区间，interval0 为尾迭代器
Map.Entry<Integer, Integer> interval0 = intervals.floorEntry(val);
interval0.getKey();    interval0.getValue()
```



###### String int转换

```java
//String->Int
String str = "123";
int a = Integer.parseInt(str);
System.out.println(a+"//end");

//Int->String
String str2 = Integer.toString(a);

String str3 = String.valueOf(a);
System.out.println(str2+","+str3);
```

###### char int计算

```
int a = 'b' - 'a';
char b = (char)('0'+num);

//char判断字母符号
Character.isLetterOrDigit(b);
Character.isLetter(b); //true false
Character.toLowerCase(b);  
Character.toUpperCase(b);  
```

###### String 

```java
String a = "abe";
String b = "abc";
System.out.println(a.compareTo(b)); // 2  >0  a>b

a.substring(0,2);  //左闭右开 都是索引

//String->char[]
char[] cs = a.toCharArray();
//char[]->String
String css = new String(cs);

//返回空String
return new String("")
char a='c';
String b = ""+a; //""+char -> String
//path 为 Deque<String>型 几个String片段 用String.join(连接符,拼接数组/队列)
//path 改为List<String>等也都可以
String.join(".", path);

//判断是否为前缀
w1.startsWith(w2);
```



###### StringBuffer

```java
StringBuffer path = new StringBuffer(0);
path.append('(');
path.delete(path.length()-1,path.length()); // delete 左闭右开 [,)
new String(path);
path.toString();
//path为List<Character> 时也可以用path.toString();
```



###### new int[]

```
new int[] {2,3,4}
new int[2]; //默认是0
```



###### List

```
public static void main(String[] args){
    List<String>list = new ArrayList<String>();
    list.add("草莓");  //向列表中添加数据
    list.add("香蕉");  //向列表中添加数据
    list.add(1,"菠萝");  //向列表中添加数据
    for(int i=0;i<list.size();i++){  //通过循环输出列表中的内容
    System.out.println(i+":"+list.get(i));
  }
  String o = "苹果";
  System.out.println("list对象中是否包含元素"+o+":"+list.contains(o));  //判断字符串中是否包含指定字符串对象
}

//List更新
list.set(index,val);
//排序
Collections.sort(list); 

//二维List添加-一行版
List<List<Integer>> res = new ArrayList<>();
res.add(new ArrayList<>(Arrays.asList(1,2)));
```



###### 运算符？：

注意?:的级别较低 

a=b?0:3 + 5; //即a=b?0:8



###### ACM模式处理输入输出

```
import java.util.*;

//https://leetcode-cn.com/problems/gou-jian-cheng-ji-shu-zu-lcof/submissions/
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

//enter class->public!
public class ACMdemo {
    public static void main(String[] args) {
        // write your code here
        Solution solution = new Solution();

        Scanner sc=new Scanner(System.in);

        while (sc.hasNext()){
            String templine = sc.nextLine();
            System.out.println(templine);
            if(templine.equals("")){
                continue;
            }
            //
            String[] inputStr = templine.split(",");
//            System.out.println(Arrays.toString(inputStr));
            int[] a = new int[inputStr.length];
            //leetcode enter
            for(int ii=0;ii<a.length;ii++){
                a[ii] = Integer.parseInt(inputStr[ii]);
            }
            int[] b = solution.constructArr(a);
            //
            System.out.println(Arrays.toString(b));
        }

    }
}
```

