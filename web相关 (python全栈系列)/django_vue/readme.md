# Django+Vue 前后端分离工程

1. 前端Vue //在vue1子目录下

   - 多组件单入口

   - axios通信

   - 运行说明，首先安装node和npm，推荐cnpm :  ` npm install -g *cnpm* --registry=https://registry.npm.taobao.org`，然后cnpm install

   - 开发时运行npm start，部署时运行npm run build（main.js中axios.defaults.baseURL需修改，详见注释）, 且django已调为开发时兼容允许跨域模式

   - 采用local Storage存储登录信息，可以继续在留出的接口写后端的token加密，防止伪造登录信息

   - 退出登录（logout）在HelloWorld.vue中，采用一个

     ```javascript
     <router-link :to="{ path: '/', query: { logout: '1' }}">退出登录</router-link>
     ```

     实现跳转到登录界面+传参，而登陆界面在钩子函数中

     ```
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
     ```

     实现了检测logout字典参数并清空storage的功能，巧妙实现退出

   - 利用this.username更新数据、利用`<router-link to="/xx">ab</router-link> `实现vue内页面跳转等

2. 后端Django(api) 

   - 需安装django>=2.2.0，和` pip install django-cors-headers`

   - django1/settings.py中注明静态文件、模板文件目录和/索引位置

   - django1只利用了其api功能，方便移植到express(node.js)等其他后端

   - 登录方面留出token添加接口，token验证思路是每一次后端请求时，都会传来username和token，查找username对应的上一次的token，判断相同则更新时间和token并提供相应后端服务；如果超时则清空token时间戳并返回拒绝信息

     其中更新方案为更新时间戳，并重新利用时间戳+密钥=》token，保存本地并返回给前端更新

3. 数据库方案选择

   - 目前选择是利用app1/config.py，读写本地ini文件，方便快捷免部署
   - 如果数据量大，推荐采用mongodb，为了减小后端耦合，可以方便采用pymongo进行读写，代码量也是短短几行几乎一样。mongodb的非结构型数据库更有利于开发效率



- Vue+django的策略方便了前端开发，也让前后端分离项目变得形散神不散、更加健壮

- 部分参考：` https://zhuanlan.zhihu.com/p/25080236?open_source=weibo_search`