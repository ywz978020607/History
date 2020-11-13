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
    <h2>Essential Links</h2>
    <!-- <a href="/HelloWorld">Hello</a>
    <a href="/">Login</a> -->
    <router-link to="/HelloWorld">Hello</router-link>
    <router-link to="/">Login</router-link>
    



    <ul>
      <li>
        <a
          href="https://vuejs.org"
          target="_blank"
        >
          Core Docs
        </a>
      </li>
      <li>
        <a
          href="https://forum.vuejs.org"
          target="_blank"
        >
          Forum
        </a>
      </li>
      <li>
        <a
          href="https://chat.vuejs.org"
          target="_blank"
        >
          Community Chat
        </a>
      </li>
      <li>
        <a
          href="https://twitter.com/vuejs"
          target="_blank"
        >
          Twitter
        </a>
      </li>
      <br>
      <li>
        <a
          href="http://vuejs-templates.github.io/webpack/"
          target="_blank"
        >
          Docs for This Template
        </a>
      </li>
    </ul>
    <h2>Ecosystem</h2>
    <ul>
      <li>
        <a
          href="http://router.vuejs.org/"
          target="_blank"
        >
          vue-router
        </a>
      </li>
      <li>
        <a
          href="http://vuex.vuejs.org/"
          target="_blank"
        >
          vuex
        </a>
      </li>
      <li>
        <a
          href="http://vue-loader.vuejs.org/"
          target="_blank"
        >
          vue-loader
        </a>
      </li>
      <li>
        <a
          href="https://github.com/vuejs/awesome-vue"
          target="_blank"
        >
          awesome-vue
        </a>
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
      msg: 'Welcome to Your Vue.js App'
    }
  },
  mounted(){
    console.log(localStorage.getItem('loggedname'))
    this.username= localStorage.getItem('loggedname')
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
