https://blog.csdn.net/fantacy10000/article/details/95974634

##### 头文件

- stdio.h

  #include<stdio.h>

  > c语言的标准输入输出，常用`printf;scanf`

- random

  > ```
  > #include<stdlib.h>
  > srand((unsigned)time(NULL)); 
  > (double)rand()/RAND_MAX;  //[0-1]
  > //要取得 [a,b) 的随机整数，使用 (rand() % (b-a))+ a; //考虑到均向下取整
  > //要取得 [a,b] 的随机整数，使用 (rand() % (b-a+1))+ a;
  > ```

- iostream

  > c++语言的标准输入输出，重用`cin;cout`

- algorithm

  > c++的常用算法头文件，如`sort;qsort`
  
- 最值

  #include<limits.h>  或直接自己定义  #define INT_MAX=2^31-1; INT_MIN=-2^31;

  INT_MIN   INT_MAX 
  
- #include<math.h>      #include<map> // STL引用均不加.h

- 新旧标准

  ```
  #include <stdio.h> --> #include <cstdio>
  #include <stdlib.h> --> #include <cstdlib>
  #include <string.h> --> #include <cstring>
  #include <math.h> -->  #include <cmath>
  ```

  "xx.h"是自己写的，从当前目录查找；<>是系统中的，从系统目录查找

##### 数组处理

- memcpy

  > 数组a复制k个元素到数组b：`memcpy(b,a,sizeof(int)*k);`

  > 数组a全部复制到数组b:`memcpy(b,a,sizeof(a));`

- memset

  > 数组a清0：`memset(a,0,sizeof(a));`
  >
  > 这里注意一点，memset对int数组赋初值时**只能赋值0**，其他数都不能赋值，因为memset赋值的单位是字节，而int是4个字节，所以你赋值0，每字节都是0。所以合起来4个字节也是0，但是赋值其他的数，4个字节合起来就不是原来的数了。(所以memset大多用来给char数组赋初值，因为char是一个字节)。

##### 数学计算

- pow

  > `pow(double a,double b);`
  >  头文件:`#include <math.h>` 
  >  功能:计算a的b次方

##### 字符处理

- sprintf

  > printf输出到屏幕，fprintf输出到文件，sprintf输出到字符串
  >  `sprintf（a,"%d%d%d",a,b,c);`//a为字符串数组

- tolower  toupper

  > 格式：int tolower(int c)或（char c）
  >  将大写字符转化为小写，**非字母字符不做处理**
  >  头文件:ctype.h或stdlib.h或iostream或string（4个貌似都可以..)

- strcmp

  > `int strcmp(const char *s1, const char *s2);`
  >  【功能】:比较两个字符串的大小
  >  【规则】：字符串大小的比较是以ASCII 码表上的顺序来决定，此顺序亦为字符的值。strcmp()首先将s1第一个字符值减去s2 第一个字符值，若差值为0 则再继续比较下个字符，若差值不为0 则将差值返回。例如字符串"Ac"和"ba"比较则会返回字符"A"(65)和'b'(98)的差值(－33)。
  >  【返回值】：若参数s1 和s2 字符串相同则返回0。s1 若大于s2 则返回大于0 的值。s1 若小于s2 则返回小于0 的值。
  >
  > 【注意1】：如果s1和s2长度不相等且s1是s2的子串，则s1<s2，即`strcmp(s1,s2)<0`
  >
  > 【注意2】：另外，这个函数在某些编译器上只返回-1,0,1三个值，并不是规定的返回值。所以一般用    <0,>0,=0来判断。

- string对象(c++)

  > string是c++中的字符对象。处理数组比c语言要方便很多，有几个常用的方法:
  >
  > 1. `erase(int a,int b)`:从下标a起删除b个字符
  > 2. `find(string)`:查找string出现的首下标，找不到返回std::string::npos(判断是否找到只能用s.find(str)==std::string::npos)
  > 3. `c_str()`将string对象转化为c语言字符串。
  > 4. `size()`返回字符串大小
  > 5. `substr(begin,len)`截取字符串，从下标为begin开始，截取长度为len的字符串,不加len直接截取到最后。
  > 6. `replace(begin,len,str)`从下标begin开始，长度为len的字符串替换为str
  > 7. `insert(begin,len)`从下标begin开始，插入长度为len的字符串
  > 8. 取特定下标的字符`string s;char a = s[i];`返回的是char类型。
  > 9. 翻转字符串 `reverse(a.begin(),a.end())`

- isalnum  //is a letter/num

  > 判断字符是否为字母或者数字
- 字符大小写转换 toupper(char)  tolower(char)
- char/int转string

  > 1. 将ascill码转string

  

  ```cpp
  to_string(char(‘A’+3))//直接to_string会输出“68”
  或者：
  char a；
  a = 'A'+3;
  to_string(a);
  或者char('A'+3)+""就直接转化为string
  ```

- string(char) 转int

  > 1. char转int
  >     **atoi ** //a to i

  

  ```cpp
      string s = "12";
      int a = atoi(s.c_str());
  ```

  > 1. string 转int
  >     **stoi**

  

  ```cpp
  int a = stoi(string a);
  ```

##### unsigned

​	unsigned 默认是int  和signed 运算后结果默认转为unsigned (-2^31,2^31-1)

​	size_t 代替



##### 算法

- sort

  > c++排序函数，***在std下\***，时间复杂度nlogn
  >
  > 第一个参数是要排序的区间首地址，第二个参数是区间尾地址的**下一地址**。比如有一个数组int a[100]，要对从a[0]到a[99]的元素进行排序，只要写sort(a,a+100)
  >
  > `sort(begin,end,compare(默认为升序));`
  >  `bool compare(int a, int b) { return a

- 二分查找

  > 说明：在一个前闭后开的区间里进行二分查找。
  >  1.`lower_bound(first,last,key)`
  >  2.`upper_bound(first,last,key)`
  >  3.`binary_search(first,last,key)`
  >  其中如果寻找的value存在，那么lower_bound返回一个**迭代器**指向其中第一个这个元素。upper_bound返回一个迭代器指向其中最后一个这个元素的下一个位置（明确点说就是返回在不破坏顺序的情况下，可插入value的最后一个位置）。如果寻找的value不存在，那么lower_bound和upper_bound都返回“假设这样的元素存在时应该出现的位置”。（迭代器相当于一个指针指向数组中的某个元素）
  >  binary_search试图在已排序的[first,last)中寻找元素value，若存在就返回true，若不存在则返回false。

##### c++运算符重载

- 格式说明

  > type operator sign (parameters);
  >  运算符重载定义在类或结构体内，只针对此类或结构体的具体运算。
  >  例：
  >  `struct E{`
  >  `char name[101];`
  >  `int age;`
  >  `int score;`
  >  `E operator + (E b){`
  >  `b.age = age+b.age;`
  >  `return b;`
  >  `}`
  >  `}`
  >  调用:
  >  `struct a;struct b;struct c;`
  >  1.`c = a + b;`
  >  2.`c = a.operator+(b);`

##### 输入（关于输入输出的细节需看我写的博客）

- scanf

  > tip1:`scanf("%4d%3d",&a,&b)`//输入一个数取其前四位赋给a,后四位赋给b
  >
  > tip2:
  >  在输入**数值数据或字符串（%d或%s）**时，若格式控制串中没有非格式字符作输入数据之间的间隔则可用**空格，TAB或回车**作间隔。C编译在碰到空格，TAB，回车或非法数据(如对“%d”输入“12A”时，A即为非法数据)时即认为该数据结束。
  >  在输入**单个字符数据（%c）**时，若格式控制串中无非格式字符，则认为所有输入的字符均为有效字符,这时输入时无法用空格，TAB或回车做间隔。
  >  例如：
  >
  > 1. `scanf("%c%c%c",&a,&b,&c);`输入d e f则把'd'赋予a，' ' 赋予b，'e'赋予c。只有当输入为def时，才能把'd'赋于a，'e'赋予b，'f'赋予c。
  > 2. 如果在**格式控制中加入空格作为间隔**，如：
  >     `scanf ("%c %c %c",&a,&b,&c);`
  >     则输入时各数据之间可加空格。
  > 3. 以%s输入字符串时可以以空格tab或回车做结束，如：
  >     `char a[10],b[10];`
  >     `scanf ("%s%s",a,b);`
  >     则输入时各数据之间可加空格或回车。
  >
  > tip3:
  >  scanf的格式控制部分分为三部分：1格式化说明符，2空白符，3非空白符
  >
  > 1. 格式化说明符比如%s,%c;
  > 2. 空白字符会使scanf()函数在读操作中略去输入中的一个或多个空白字符，空白符可以是space,tab,newline等等，直到第一个非空白符出现为止。
  > 3. 一个非空白字符会使scanf()函数在读入时剔除掉与这个非空白字符相同的字符。

- getchar

  > getchar函数的返回值是用户输入的字符的ASCII码，如出错返回-1.当程序调用getchar时.程序就等着用户按键.用户输入的字符被存放在键盘缓冲区中.直到用户按回车为止（回车字符也放在缓冲区中）.当用户键入回车之后，getchar才开始从stdio流中每次读入一个字符,且将用户输入的字符回显到屏幕.如用户在按回车之前输入了不止一个字符，其他字符会保留在键盘缓存区中，等待后续getchar调用读取.也就是说，后续的getchar调用不会等待用户按键，而直接读取缓冲区中的字符，直到缓冲区中的字符读完为后，才等待用户按键。
  >  **注：回车符和空格都是字符，所以也会被getchar吸收，所以经常用getchar吸收多余的回车符。**

- gets

  > `gets(a)` 是输入一个字符串，存入a.以回车做为结束，但是不以空格结束，这是和scanf的不同.和scanf的相同点是      字符串接受结束后自动加'\0'.
  >
  > 例：
  >  `#include  main() { char ch1[10],ch2[10],c1,c2; scanf("%s",ch1); c1=getchar(); gets(ch2); c2=getchar(); }`
  >  依次键入asdfg回车，asdfg回车，则ch1="asdfg\0"，c1='\n'，ch2="asdfg\0"，c2需再次输入。
  >  **scanf**：当遇到回车，空格和tab键会自动在字符串后面添加'\0'，只读取回车空格tab之前的字符。但是回车，空格和tab键仍会**留在输入的缓冲区中。**
  >  **gets**：可接受包括回车符以及之前输入的所有字符，并用'\0'替代 '\n'.回车键不会留在输入缓冲区中，因为gets会把回车一起读入，并用'/0'替换。

- cin

  > 这个是c++中的输入，头文件为``
  >  cin和scanf一样，输入的回车和空格可认为停止输入，不会读取，但都会保留在缓冲区内，需要吸收。而gets读取空格，且只以回车为结束标志。
  >  **注意**：cin比scanf耗时很多，所以许多比赛建议用scanf而不是cin

##### 输出

- puts

  > 1.puts()函数只用来输出字符串(结尾必须有'\0').没有格式控制，里面的参数可以直接是字符串或者是存放字符串的字符数组名。而printf（）函数的输出格式很多，可以根据不同格式加转义字符，达到格式化输出。
  >  2.puts（）函数的作用与语句printf("%s\n",s);的作用形同，**即自动在最后加上换行符**。

- cout

  > cout输出和c的输出不太一样，他是带缓存的，只有缓存满时才输出，利用endl就是直接输出，清空缓存。
  >  endl的作用：
  >  \1. 将换行符写入输出流，其中Unix/Linux换行符是\n，Windows中是\r\n，MAC中是\r；
  >  \2. 清空输出缓冲区。

##### STL

###### deque

(1) 构造函数

deque():创建一个空deque

deque(int nSize):**创建一个deque,元素个数为nSize**

deque(int nSize,const T& t):创建一个deque,元素个数为nSize,且值均为t

deque(const deque &):复制构造函数

(2) 增加函数

void **push_front(const T& x):双端队列头部增加一个元素X**

void **push_back(const T& x):双端队列尾部增加一个元素x**

iterator **insert**(iterator it,const T& x):双端队列中**某一元素前**增加一个元素x

void **insert**(iterator it,int n,const T& x):双端队列中**某一元素前**增加n个相同的元素x

void **insert**(iterator it,const_iterator first,const_iteratorlast):双端队列中**某一元素前**插入另一个相同类型向量的[forst,last)间的数据

(3) 删除函数

Iterator **erase**(iterator it):删除双端队列中的**某一个元素**

Iterator **erase**(iterator first,iterator last):删除双端队列中[first,last）中的元素

void pop_front():删除双端队列中**最前一个元素**

void pop_back():删除双端队列中**最后一个元素**

void clear():清空双端队列中最后一个元素

(4) 获取端值

​	.front();  .back();

###### vector

> 格式:`vector a/a(N)`
> 1.头文件``
>
> 2.功能：常用于表示图的邻接表，其功能上相当于一个一维数组。
>
> - 初始化一个vector
> `vector<int> a = {1,2,3,5}`
> `vector<int> a(n,1) //初始化一个有n个元素的数组，每个位置值为1，不是[n,1]的意思` 
>
> - 二维vector！
>
> vector<vector<int>> dp(word1.size(),vector<int>(word2.size(),0));
>
> - 向vector添加一个vector
> `<vector> a`
> `a.push_back(vector(3,1))//vector(3,1)是一个包含三个元素的vector,元素值全为1`
>
> - 排序
>   `sort(a.begin(),a.end())//默认升序`
>
> - 无索引vector
>
>   such as: `if(map1.find(vector<int> (1,0))!=map1.end())`//花括号也ok！
>
>  3.成员方法：
>
> - `push_back(value)`
> 把元素插入末尾
> - `size()`
> 返回元素的个数
> - `clear()`
> 清空vector中的元素
> - `back()`
> 取最后一个值 返回
> - `pop_back()`
> 取出最后一个值，不返回
> - `erase(iterator index)`
> 删除index指向的元素，如`erase（a.begin()+2)`//删除第3个元素

###### set

> 格式：`set s`
> 1.头文件``
> 2.功能：集合里面不允许出现重复的值
> 3.成员方法：
>
> - `insert(value)`
>
> - `second`
> 判断插入是否成功，当插入重复的元素时会返回false。代码：`if(s.insert(value).second==false) return false`
>
> - find / count
>
> - std::cout<< (set1.find(vector<int>{3,4})!=set1.end());
>
> - count 返回1或0
>
> ```
> for (auto it = s.cbegin(); it != s.cend(); it++) { 
> 		printf("%07d\n", *it);
> } 
> ```
>
> ```
> set<int> set1;
>     set1.insert(1);
>     set1.insert(0);
>     for(const int &item:set1){ //也可以用auto
>         cout<<item;
>     }
> ```
>
> 

###### map/unordered_map

> 格式：
> 1.头文件:`/`
> 2.特性：map是stl中的关联容器，他的元素是一对数据，而像set等是一个数据。map的键唯一，multimap键可以不唯一，内部用红黑树实现，所以是按二叉搜索树严格排序的，查找效率达不到java中hash_map的O(1),为O(logn)。而unordered_map内部是hash表实现的，查找效率可以达到O(1)。
> 3.格式:`map\unordered_map m`
> 4.成员方法:
>
> - 插入
>
> `默认是0  可以直接m[2] += 1;`
>
> `m[2] = 212\\如果键值2已存在，则更新相应的值`
> `m.insert({ 'd', 100 })`
>
> `m.insert(make_pair('d',100))`
>
> -- 也可以用pair
>
> - 判空
> `empty()`
>
> - 索引
>
> `m[key]`
>
> - 查找
>   `iterator find (key);\\如果找到则返回该迭代器，否则返回end()`
>   `if(m.find(key)!=m.end())`
>
>   `m.count(key)==1 or 0`
>
> - 遍历
>
> ```
> //迭代器 (指针->first)
> std::map<string, string>::iterator  it;
> for (it = mapSet.begin(); it != mapSet.end(); ++it)
> {
>     std::cout << "key" << it->first << std::endl;
>     std::cout << "value" << it->second << std::endl;
> }
> //or 引用 (entry.first)
> for(auto &entry : mapSet){ //auto可以换成const pair<int,int> 
> 	cout<< entry.second; //first second
> }
> ```
>
> - 删除
>
>   m.erase(key);

###### pair

`#include<utility>`

类似容器，pair<T1,T2> val;

//初始化方法

``` 
pair<string,string> demo("123","345"); //{} 也可以用() 
pair<string,string> demo = {"123","345"};//用=的话必须用{}  only
pair<string,string> ("123","345"); //{} 也可以用() -> 直接创建 建议{}  像vector用()表示的是数量

//不需要显示定义<T1,T2>类型
make_pair("123","456");
```



###### priority_queue

https://leetcode-cn.com/problems/hua-dong-chuang-kou-de-zui-da-zhi-lcof/solution/hua-dong-chuang-kou-de-zui-da-zhi-by-lee-ymyo/

> 格式:`priority_queue p`
> 1.头文件``
> 2.功能：优先队列，出队列不再是先进先出，而是优先级最高的先出。内部原理是堆（大顶堆或小顶堆）
> 3.成员方法：
>
> - `push(value)`
>   把元素插入末尾
>
> - `size()`
>   返回元素的个数
>
> - `pop()`
>   队首元素（优先级最高）出队列
>
> - `top()`
>   返回队尾元素（优先级最低)
>   **注意1**：`priority_queue`默认是大顶堆，`priority_queue,greater >`是建立一个小顶堆(多加两个参数）。另外，如果是结构体类型，可以在结构体中重载 '<' 号，重定义优先级。类似sort，不过和sort的 '<' 号功能正好相反。看题1416代码。
>   **注意2**：**top（）返回的元素不能直接修改**。即类似`s.top()--`这种是错误的。只能先赋值给其他对象再修改再存进去。如`q = s.top();q--;s.pop();s.push(q);`这个规则也适合其他STL的top()函数
>
>   ```
>   int main() {
>       std::cout << "Hello World!\n";
>       struct cmp
>   {
>   	//只能是T &a,T &b  如果其他的话可以封装为struct再导入
>       bool operator()(int &a, int &b) const
>       {
>           //因为优先出列判定为!cmp，所以反向定义实现最小值优先
>           return a > b; //小顶堆-最小优先
>       }
>   };
>       std::priority_queue<int, std::vector<int>, cmp> pq;
>       pq.push(3);
>       pq.push(4);
>       pq.push(5);
>       std::cout<<pq.top();
>   }
>   ```
>
>   如果默认=>最大优先队列（默认也是大顶堆），如果加入第三参数为greater<>或者按上文改入，则为最小优先！



##### 一些方法

- 给一个数组全赋值0的方法

  > 1.memset(..);
  >  2.int a[100] = {0};//这个较简便

- 刷题过程中经常碰到二元坐标，可以用pair解决

  ```
  typedef pair<int,int> Point; //否则要自己写个类+构造函数等
  
  ```

  