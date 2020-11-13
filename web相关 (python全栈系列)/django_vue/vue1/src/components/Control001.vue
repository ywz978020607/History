<template>
  <div class="hello">
  <link rel="stylesheet" type="text/css" href="../../static/css/bar.css">
    <header id="top">
    <div class ="top_box">
        <ul class="lf">
            <li><a href="#">欢迎</a></li>
            <li><a href="#">Welcome!</a></li>
        </ul>
        <ul class="rt">
                <li>用户名: {{username}} </li>
                <li><router-link :to="{ path: '/', query: { logout: '1' }}">退出登录</router-link></li>
                <!-- <li><a href="{% url 'login' %}">登录</a></li> -->
                <!-- <li><a href="{% url 'register' %}">注册</a></li> -->
        </ul>
    </div>
    </header>
<!-- //////////////////////// -->


    <img src="../assets/logo.png">
    <h1>{{ msg }}</h1>
    <h2>远程遥控</h2>
    <p>当前状态数值 : {{remote_status}} </p>
    <br><br><br>
    <ul>
      <li>
        <el-button  v-on:click="click1">远程开启</el-button>
        <el-button  v-on:click="click2">远程关闭</el-button>
        <el-button  v-on:click="click3">待用3</el-button>
        <el-button  v-on:click="click4">待用4</el-button>
      </li>
    </ul>
  </div>
</template>

<script>


export default {
  name: 'HelloWorld',
  data () {
    return {
      username:'',
      msg: 'Welcome to Your Vue.js App',
      remote_status:'-',
    }
  },
  mounted(){
    console.log(localStorage.getItem('loggedname'))
    this.username= localStorage.getItem('loggedname')
    this.timer = setInterval(this.myget,2000); //定时器启动
  },
  methods: {
    click1(){
      console.log("click")
      // this.$axios({
      //           url:'/onenet_write/',
      //           method:'get',
      //           params:{
      //               id: '617422839',
      //               password: 'gjU2173SbsvrSi4OpLyK8IXW3tc=',
      //               data_value:JSON.stringify(['1']),
      //               data_name:JSON.stringify(['lock']),
      //           },
      //           headers: {
      //             'Content-Type': 'application/json'
      //           },
      //         }).then(res=>{
      //           alert("ok");
      //         })
          this.$axios({
                url:'/',
                method:'get',
                params:{
                    username:this.username,
                    data_value:'1',
                    mode:"remote_write"
                },
                headers: {
                  'Content-Type': 'application/json'
                },
              }).then(res=>{
                alert("ok");
              })
    },
    click2(){
      console.log('click')
      this.$axios({
                url:'/',
                method:'get',
                params:{
                    username:this.username,
                    data_value:'0',
                    mode:"remote_write"
                },
                headers: {
                  'Content-Type': 'application/json'
                },
              }).then(res=>{
                alert("ok");
              })
    },
    click3(){
      console.log("click")
    },
    click4(){
      console.log("click")
    },
    // url="http://api.heclouds.com/devices/611890860/datapoints"
    // headers={'api-key':'gjU2173SbsvrSi4OpLyK8IXW3tc='}
    myget(){
      this.$axios({
                url:'/',
                method:'get',
                headers: {
                 'Content-Type': 'application/json'
                },
                params:{
                  username:this.username,
                  mode:"remote_check",
                  // 'limit_num':'1',
                  // 'id':'617422839',
                  // 'password':'gjU2173SbsvrSi4OpLyK8IXW3tc=',
                }
              }).then(res=>{
                console.log(res.data);
                console.log(res.data.data.datastreams[0].datapoints[0].value)
                status = res.data.data.datastreams[0].datapoints[0].value;
                this.remote_status = status;
              })

    },
    
  }


}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
