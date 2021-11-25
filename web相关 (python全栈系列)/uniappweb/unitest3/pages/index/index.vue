<template>
    <div class="flex-center">
            <div class="container">
                <div class="flex-center">
                    <div class="unit-1-2 unit-1-on-mobile">
                        <p>登陆界面</p>

                        <div v-if="tips">--------{{ tips }}---------------</div>

                        <div class="form">
                            <!--  {% csrf_token %} -->
                            <p>用户名:<input style="border:1px solid #d2d2d2;" type="text" name='username' v-model="input_val[0]"></p>
                            <p>密 码:<input type="password" name='password' v-model="input_val[1]"></p>

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
</template>

<script>
	export default {
		data() {
			return {
			  motto: 'Hello',
			  ////
			  mode: 0, //0登录，1改密，2注册,3退出
			  tips: "",
			  input_val: [null, null, null, null], //初始4个null
			  direction: "http://192.168.137.1:8000/api/"
			}
		},
		onLoad() {
		console.log("onload ok.")
		// alert("123")
		
		
		},
		methods: {
    button1(event) {
					console.log(this.mode);
                         var that = this; //注意，http请求后的函数中，this的指向为副本的局部，无法真正修改！！所以要用that先复制指针，用that改值
 
                         console.log(that.input_val)
                         if (this.mode == 0) {
                             //登录
                             console.log("logging.")
                             var param = {
                                 "mode": "0",
                                 "data": JSON.stringify(that.input_val)
                             }
                             console.log(param);
							 //http requests
							 uni.request({
								url: this.direction, 
								data:param,
								header: {'content-type': 'application/x-www-form-urlencoded'},
								method:'POST',//请求方式  或GET，必须为大写
								success: res => {
										console.log('返回', res.data);
										if(res.data["status"]=="ok"){
											var url = "../first/index?username="+that.input_val[0];
											uni.navigateTo({url});
										}
										else{
											alert("失败")
										}
								 },
								 fail:res =>{
									 alert("失败")
								 },
                             });
							 
						//end mode=0
                         };
						 
						 if (this.mode == 1) {
						      //改密
						      console.log("logging.")
						      var param = {
						          "mode": "1",
						          "data": JSON.stringify(that.input_val)
						      }
						      console.log(param);
						 	 //http requests
						 	 uni.request({
						 	 				url: this.direction, 
						 					data:param,
						 					header: {'content-type': 'application/x-www-form-urlencoded'},
						 	                method:'POST',//请求方式  或GET，必须为大写
						 	 				success: res => {
						 	 						console.log('返回', res.data);
						 							if(res.data["status"]=="ok"){
						 								alert("成功")
														that.mode=0;
						 							}
						 							else{
						 								alert("失败")
						 							}
						 					 },
						 	                 fail:res =>{
						 	                     alert("失败")
						 	                 },
						      });
						 	 
						 //end mode=1
						  }
						  
						  if (this.mode == 2) {
						       //注册
						       console.log("logging.")
						       var param = {
						           "mode": "2",
						           "data": JSON.stringify(that.input_val)
						       }
						       console.log(param);
						  	 //http requests
						  	 uni.request({
						  	 				url: this.direction, 
						  					data:param,
						  					header: {'content-type': 'application/x-www-form-urlencoded'},
						  	                method:'POST',//请求方式  或GET，必须为大写
						  	 				success: res => {
						  	 						console.log('返回', res.data);
						  							if(res.data["status"]=="ok"){
						  								alert("成功")
						  								that.mode=0;
						  							}
						  							else{
						  								alert("失败")
						  							}
						  					 },
						  	                 fail:res =>{
						  	                     alert("失败")
						  	                 },
						       });
						  	 
						  //end mode=2
						   }
						 
						 
                    },
		}
	}
</script>

<style>
	
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 200rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>
