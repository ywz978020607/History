<template>
  <div @click="clickHandle">

    <!-- <div class="userinfo" @click="bindViewTap">
      <img class="userinfo-avatar" v-if="userInfo.avatarUrl" :src="userInfo.avatarUrl" background-size="cover" />
      <img class="userinfo-avatar" src="/static/images/user.png" background-size="cover" />

      <div class="userinfo-nickname">
        <card :text="userInfo.nickName"></card>
      </div>
    </div> -->
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
      motto: 'Hello',
      userInfo: {
        nickName: '',
        avatarUrl: 'http://mpvue.com/assets/logo.png'  //no use
      },
      ////
      username:'',
      mode: 0, //0登录，1改密，2注册,3退出
      tips: "",
      input_val: [null, null, null, null], //初始4个null
      direction: "http://207.148.124.188:8000/api/"
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
    var url = "../first/index?id=" + 5
    wx.navigateTo({url})
    }
  },

  created () {
    let app = getApp()
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
