<template>
  <body id="poster">
    <el-form class="login-container" label-position="left" label-width="0px">
      <h3 class="login_title">欢迎访问</h3>
      <el-form-item>
        <el-input type="text" v-model="loginForm.username" auto-complete="off" placeholder="账号"></el-input>
      </el-form-item>
 
      <el-form-item>
        <el-input type="password" v-model="loginForm.password" auto-complete="off" placeholder="旧密码"></el-input>
      </el-form-item>
 
      <el-form-item>
        <el-input type="password" v-model="loginForm.password2" auto-complete="off" placeholder="新密码"></el-input>
      </el-form-item>
 
      <el-form-item style="width: 100%">
        <el-button type="primary" style="width: 100%;background: #505458;border: none" v-on:click="changepwd">改密</el-button>
      </el-form-item>
      <el-form-item  style="height:0px">
      <router-link to="/" style="width: 50%" ><span style="float:left">登录</span></router-link>
      <router-link to="/Register" style="width: 50%" ><span style="float:right">注册</span></router-link>
      </el-form-item>
    </el-form>
  </body>
</template>
 
 
<script>
    export default {
        name: "ChangePwd",
        data() {
            return {
                loginForm: {
                    username: '',
                    password: '',
                    password2: '',
                    
                },
                responseResult: []
            }
        },
        methods: {
            changepwd() {
              this.$axios({
                url:'/',
                method:'post',
                data:{
                    username: this.loginForm.username,
                    password: this.loginForm.password,
                    password2: this.loginForm.password2,
                },
                headers: {
                  'Content-Type': 'application/json'
                },
                params:{
                  mode:"changepwd"
                },
              }).then(res=>{
                console.log(res.data);
                if(res.data['status']=='ok'){
                  alert("ok");
                  //查询
                  this.$router.push("/")
                }
                else{
                  alert("wrong!")
                }
              })


            }
        }
    }
</script>
 
<style>
  #poster {
    background:url("../assets/eva.jpg") no-repeat;
    background-position: center;
    height: 100%;
    width: 100%;
    background-size: cover;
    position: fixed;
  }
  body{
    margin: 0px;
    padding: 0;
  }
 
  .login-container {
    border-radius: 15px;
    background-clip: padding-box;
    margin: 90px auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
  }
 
  .login_title {
    margin: 0px auto 40px auto;
    text-align: center;
    color: #505458;
  }
 
 
</style>