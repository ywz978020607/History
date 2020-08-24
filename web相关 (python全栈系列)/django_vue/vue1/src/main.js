// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

// 设置反向代理，前端请求默认发送到 http://localhost:8443/api
var axios=require('axios')
axios.defaults.baseURL='/api'  //需要被修改 调试时使用如'http://localhost:8000/api' 部署时为'/api' 
Vue.prototype.$axios = axios
Vue.config.productionTip = false
/*作用是阻止vue 在启动时生成生产提示。*/
Vue.use(ElementUI);

Vue.config.productionTip = false

// 路由判断登录 根据路由配置文件的参数
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireAuth)){ // 判断该路由是否需要登录权限
   if (localStorage.loggedname) { // 判断当前的token是否存在 ； 登录存入的token
    next();
   }
   else {
    console.log('需要登录');
    alert("需要登录")
    next('/')
   }
  }
  else {
   next();
  }
 });


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
