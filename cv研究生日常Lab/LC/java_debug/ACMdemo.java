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
