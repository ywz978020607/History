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
    <div class="flex-center">
            <div class="container">
                <div class="flex-center">
                    <div class="unit-1-2 unit-1-on-mobile">
                        <p>登陆界面</p>

                        <div v-if="tips">--------{{ tips }}---------------</div>

                        <div class="form">
                            <!--  {% csrf_token %} -->
                            <div>用户名:<input type="text" name='username' v-model="input_val[0]"></div>
                            <div>密 码:<input type="password" name='password' v-model="input_val[1]"></div>

                            <div v-if="mode==2">确认密码:<input type="password" name='password2' v-model="input_val[2]"></div>

                            <div v-if="mode==1">新密码:<input type="password" name='new_password' v-model="input_val[3]"></div>

                            <button class="btn btn-primary btn-block" @click="button1">确定</button>
                        </div>
                        <div class="flex-left top-gap text-small">
                            <div class="unit-2-3" v-if="mode==0">
                                <a @click="mode=1">修改密码</a>
                            </div>
                            <div class="unit-1-3 flex-right" v-if="mode==0">
                                <a @click="mode=2">注册</a>
                            </div>

                            <div class="unit-2-3" v-if="mode==1">
                                <a @click="mode=0">登录</a>
                            </div>
                            <div class="unit-1-3 flex-right" v-if="mode==1">
                                <a @click="mode=2">注册</a>
                            </div>

                            <div class="unit-2-3" v-if="mode==2">
                                <a @click="mode=1">修改密码</a>
                            </div>
                            <div class="unit-1-3 flex-right" v-if="mode==2">
                                <a @click="mode=0">登录</a>
                            </div>



                        </div>
                    </div>
                </div>
            </div>
        </div>

    <!-- <button @click="click1">测试1</button> -->

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

export default {
  data () {
    return {
      motto: 'Hello',
      userInfo: {
        nickName: '',
        avatarUrl: 'http://mpvue.com/assets/logo.png'  //no use
      },
      ////
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
button1(event) {
  console.log(this.mode);
                        var that = this; //注意，http请求后的函数中，this的指向为副本的局部，无法真正修改！！所以要用that先复制指针，用that改值

                        console.log(that.input_val)
                        if (this.mode == 0) {
                            //登录
                            console.log("logging.")
                                // 提交到后端
                            // $.ajaxSettings.async = false; //修改为同步请求！！！
                            // that.input_val[0] = null;
                            var param = {
                                "mode": "0",
                                "data": JSON.stringify(that.input_val)
                            }
                            console.log(param);
                            
                            this.$httpWX.post({
                              url: that.direction,
                              data: param,
                            }).then(data => {
                              console.log(data)
                              if(data.status=='ok'){
                                console.log("ok")
                                wx.showToast({
                                  title: '登陆成功',
                                  icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
                                  duration: 2000     
                                })  
                                //跳转
                                var url = "../first/main?username="+that.input_val[0]
                                wx.navigateTo({url})
                              }
                              else{
                                wx.showToast({
                                  title: '登陆失败',
                                  icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
                                  duration: 2000     
                                })  
                              }
                            })

                        }
                        //改密
                        if (this.mode == 1) {
                            console.log("changing.")
                                // 提交到后端
                            //$.ajaxSettings.async = false; //修改为同步请求！！！
                            // that.input_val[0] = null;
                            var param = {
                                "mode": "1",
                                "data": JSON.stringify(that.input_val)
                            }
                            console.log(param);

                            this.$httpWX.post({
                              url: that.direction,
                              data: param,
                            }).then(data => {
                              console.log(data)
                              if(data.status=='ok'){
                                console.log("ok")
                                wx.showToast({
                                  title: '改密成功',
                                  icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
                                  duration: 2000     
                                })  
                                //跳转
                                
                              }
                              else{
                                wx.showToast({
                                  title: '请重试',
                                  icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
                                  duration: 2000     
                                })  
                              }
                            })
                        }
                        //注册
                        if (this.mode == 2) {
                            console.log("registering.")
                                // 提交到后端
                            // $.ajaxSettings.async = false; //修改为同步请求！！！
                            // that.input_val[0] = null;
                            var param = {
                                "mode": "2",
                                "data": JSON.stringify(that.input_val)
                            }
                            console.log(param);

                            this.$httpWX.post({
                              url: that.direction,
                              data: param,
                            }).then(data => {
                              console.log(data)
                              if(data.status=='ok'){
                                console.log("ok")
                                wx.showToast({
                                  title: '注册成功',
                                  icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
                                  duration: 2000     
                                })  
                                //跳转
                                
                              }
                              else{
                                wx.showToast({
                                  title: '注册失败',
                                  icon: 'none',    //如果要纯文本，不要icon，将值设为'none'
                                  duration: 2000     
                                })  
                              }
                            })

                        }
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
    var url = "../first/main"
    wx.navigateTo({url})
    }
  },

  created () {
    // let app = getApp()
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
