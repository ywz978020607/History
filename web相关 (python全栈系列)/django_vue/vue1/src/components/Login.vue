<template>
  <body id="poster">
    <el-form class="login-container" label-position="left" label-width="0px">
      <h3 class="login_title">欢迎访问</h3>
      <el-form-item>
        <el-input type="text" v-model="loginForm.username"  auto-complete="off" placeholder="账号"></el-input>
        <!-- <br/><br/> -->
      </el-form-item>  
      <el-form-item>
        <el-input type="password" v-model="loginForm.password"  auto-complete="off" placeholder="密码"></el-input>
      </el-form-item>
 
      <el-form-item style="width: 100%">
        <el-button type="primary" style="width: 100%;background: #505458;border: none" v-on:click="login">登录</el-button>
      </el-form-item>
      <el-form-item  style="height:0px">
      <router-link to="/ChangePwd" style="width: 50%" ><span style="float:left">改密</span></router-link>
      <router-link to="/Register" style="width: 50%" ><span style="float:right">注册</span></router-link>
      </el-form-item>
    </el-form>
  </body>
</template>
 
 
<script>
    export default {
        name: "Login",
        data() {
            return {
                loginForm: {
                    username: '',
                    password: ''
                },
                responseResult: []
            }
        },
        methods: {
            login() {
              this.$axios({
                url:'/',
                method:'post',
                data:{
                    username: this.loginForm.username,
                    password: this.loginForm.password
                },
                headers: {
                  'Content-Type': 'application/json'
                },
                params:{
                  mode:"login"
                },
              }).then(res=>{
                console.log(res.data);
                if(res.data['status']=='ok'){
                  //记录
                  localStorage.setItem('loggedname',this.loginForm.username)
                  console.log("welcome:"+this.loginForm.username)
                  //查询
                  // localStorage.setItem('loggedname','12345')
                 // localStorage.getItem('loggedname')
                //  try{
                //    localStorage.removeItem('token')
                //  }
                //  catch(e){
                //    console.log(e);
                //  }
                  // this.$router.push("/homepage")
                  if(res.data['url_mode']=='0'){
                    //前端路由
                    this.$router.push(res.data['jump'])
                  }
                  else{
                    window.location.href = res.data['jump'];
                  }
                }
                else{
                  alert("wrong!")
                }
              })
              
              // //表单提交
              // let formData = new FormData();
              // formData.append('username', '123');
              // formData.append('categoryName', "1234");
              // this.$axios({
              //   url:'/',
              //   method:'post',
              //     data:{
              //       username: this.loginForm.username,
              //       password: this.loginForm.password
              //   },
              //   headers: {
              //     'Content-Type': 'application/x-www-form-urlencoded'
              //   },
                
              //   params:{
              //     mode:"login"
              //   },
              // }).then(res=>{
              //   console.log(res.data);
              // })

            }
        },
        
        mounted(){
          //logout
          try{
              if(this.$route.query.logout){
                console.log("登出")
                try{
                   localStorage.removeItem('loggedname')
                   localStorage.removeItem('token')
                 }
                 catch(e){
                   console.log(e);
                 }
              }
          }
          catch(e){
            console.log(e);
          }
        },
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