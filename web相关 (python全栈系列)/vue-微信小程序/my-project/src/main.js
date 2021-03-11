import Vue from 'vue'
import App from './App'

//css
import "../static/mobi.min.css"

import "../static/ywz_index.css"
// import "../static/bootstrap.css"
// import "../static/table.css"

//引用request
import WXrequest from './utils/wx-request'
Vue.prototype.$httpWX = WXrequest

Vue.config.productionTip = false
App.mpType = 'app'

const app = new Vue(App)
app.$mount()