<template>
  <div @click="clickHandle">
    <header id="top" style="font-size: 10px;">
            <!-- 内容显示区域 ：width : 1211px -->
            <div id="top_box">
                <ul class="lf">
                    <li><a href="#">欢迎</a></li>
                    <li><a href="#">Welcome!</a></li>
                </ul>
                <ul class="rt">
                    <li>用户名: {{ username }}</li>
                    <li><a @click="quit">退出登录</a></li>

                </ul>
            </div>
        </header>
        <!-- body-block -->


    {{username}}
    <p>First</p>
    
  
    <button @click="click1">测试1</button>

    <!-- <div class="all">
        <div class="left">
        </div>
        <div class="right">
        </div>
    </div> -->
  </div>
</template>

<script>
import card from '@/components/card'


export function getQuery() {
  /* 获取当前路由栈数组 */
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const options = currentPage.options
  return options
} 

export default {
  data () {
    return {
      username: "",
      intervalId: null,
      seen_id: 0,
      seen_table1: 0,
      //////////////
      val: [
          0, 1
      ],
      //// 
      input_val: [null, null, null, null, null, null, null, null], //初始8个null
      res_data: [],
      res_data1: [], 
      res_data2: [], 
      temperature: "",
      humidity: "",
      temptime: "",

      direction: "http://127.0.0.1:8000"

    }
  },

  components: {
    card
  },

  methods: {
    bindViewTap () {
      const url = '../logs/main'
      if (mpvuePlatform === 'wx') {
        mpvue.switchTab({ url })
      } else {
        mpvue.navigateTo({ url })
      }
    },
    clickHandle (ev) {
      console.log('clickHandle:', ev)
      // throw {message: 'custom test'}
    },
//////////////////////////////////
    quit(event) {
          var url = "../index/main"
          wx.navigateTo({url})
    },
    fresh() {
        console.log("fresh ")
    },
    // 定时刷新数据函数
    dataRefresh() {
        // 计时器正在进行中，退出函数
        if (this.intervalId != null) {
            return;
        }
        // 计时器为空，操作
        this.intervalId = setInterval(() => {
            console.log("刷新 " + new Date());
            this.fresh(); //加载数据函数
        }, 5000);
    },
    // 停止定时器
    clear() {
        clearInterval(this.intervalId); //清除计时器
        this.intervalId = null; //设置为null
    },



click1 (ev){
      console.log('click1');
      //
    //   this.$httpWX.post({
    //   url: 'http://207.148.124.188:8000/test/',
    //   data: {
        
    //   }
    // }).then(res => {
    //   console.log(res)
    // })
      //
    }
  },

  created () {
    let app = getApp()
    //定时刷新
    // this.dataRefresh();
  },
  mounted(){
    var jumpdata = getQuery()
    console.log(jumpdata)
    this.username = jumpdata.username
  }
}
</script>

<style scoped>
.userinfo {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.userinfo-avatar {
  width: 128rpx;
  height: 128rpx;
  margin: 20rpx;
  border-radius: 50%;
}

.userinfo-nickname {
  color: #aaa;
}

.usermotto {
  margin-top: 150px;
}

.form-control {
  display: block;
  padding: 0 12px;
  margin-bottom: 5px;
  border: 1px solid #ccc;
}
.all{
  width:7.5rem;
  height:1rem;
  background-color:blue;
}
.all:after{
  display:block;
  content:'';
  clear:both;
}
.left{
  float:left;
  width:3rem;
  height:1rem;
  background-color:red;
}

.right{
  float:left;
  width:4.5rem;
  height:1rem;
  background-color:green;
}
</style>
