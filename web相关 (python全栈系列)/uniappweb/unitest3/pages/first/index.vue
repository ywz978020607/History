<template>
	<div>
	        <header id="top">
	            <!-- 内容显示区域 ：width : 1211px -->
	            <div id="top_box">
	                <ul c<!-- lass="lf">
	                    <li><a href="#">欢迎</a></li>
	                    <li><a href="#">Welcome!</a></li>
	                </ul> -->
	                <ul class="rt">
	                    <li>用户名: {{ username }}</li>
	                    <li><a @click="quit">退出登录</a></li>
	
	                </ul>
	            </div>
	        </header>
	        <!-- body-block  -->
	
	        <center>
	            <br> <br>
	                <button class="btn btn-primary" @click="seen_id=0">查询系统</button> &nbsp;&nbsp;&nbsp;&nbsp;
					<button v-if="username.slice(0,5)=='admin'" class="btn btn-primary" @click="seen_id=1;">修改信息</button> &nbsp;&nbsp;&nbsp;&nbsp;
	                <button v-if="username.slice(0,5)=='admin'" class="btn btn-primary" @click="seen_id=2;click2();">查询记录</button> &nbsp;&nbsp;&nbsp;&nbsp;
	                <br> <br> <br>
	
	                <div v-if="seen_id==0">
	                    <p>当前时间{{res_time}}</p>
	                    <br>
	                    <h2>查询系统</h2>
	                    <br>
	                    <div>
	
	                        <table border="1">
	                            <tr>
	                                <td>设备号</td>
	                                <td>更新时间</td>
	                                <td>温度</td>
	                                <td>湿度</td>
	                                <td>光强</td>
	                                <td>光强阈值</td>
	                                <td>光强报警</td>
	                                <td>烟雾</td>
	                                <td>烟雾阈值</td>
	                                <td>烟雾报警</td>
	                                <td>备注</td>
	                                <td v-if="username.slice(0,5)=='admin'">提醒邮箱</td>
	
	                            </tr>
	                            <tr v-for="(each,index) in res_data1">
	                                <td>
	                                    <p v-text="each[0]"></p>
	                                </td>
	                                <td>
	                                    <p v-text="each[1].slice(0,10)+' ' +each[1].slice(11,19)"></p>
	                                </td>
	
	                                <td>
	                                    <p v-text="each[2]"></p>
	                                </td>
	
	                                <td>
	                                    <p v-text="each[3]"></p>
	                                </td>
	                                <td>
	                                    <p v-text="each[4]"></p>
	                                </td>
	                                <td>
	                                    <p v-text="each[5]"></p>
	                                </td>
	                                <td>
	                                    <span v-if="each[6]==0">正常 </span>
	                                    <span v-else>警报&nbsp;&nbsp;&nbsp;&nbsp; 时间：{{each[10].slice(0,10)+' ' +each[10].slice(11,19)}}</span>
	                                </td>
	                                <td>
	                                    <p v-text="each[7]"></p>
	                                </td>
	                                <td>
	                                    <p v-text="each[8]"></p>
	                                </td>
	                                <td>
	                                    <span v-if="each[9]==0">正常 </span>
	                                    <span v-else>警报&nbsp;&nbsp;&nbsp;&nbsp; 时间：{{each[10].slice(0,10)+' ' +each[10].slice(11,19)}}</span>
	                                </td>
	                                <td>
	                                    <p v-text="each[12]"></p>
	                                </td>
	                                <td v-if="username.slice(0,5)=='admin'">
	                                    <p v-text="each[11]"></p>
	                                </td>
	
	                            </tr>
	                        </table>
	                        <br><br>
	                        <button class="btn btn-primary" @click="click1">查询</button>
	                    </div>
	
	                </div>
	
	                <div v-if="seen_id==1">
	
	                    <p>
	                        <p>设备号 <input v-model="input_val[0]"></p>
	                    </p>
	                    <p>光强阈值 <input v-model="input_val[1]"></p>
	                    <p>烟雾阈值 <input v-model="input_val[2]"></p>
	                    <p>备注信息 <input v-model="input_val[3]"></p>
	                    <p>
	                        <p>通知邮箱 <input v-model="input_val[4]"></p>
	                    </p>
	
	                    </table>
	                    <br><br>
	
	                    <button class="btn btn-primary" @click="change">修改</button>
	                </div>
	
	
	                <div v-if="seen_id==2">
	                    <button v-if="username.slice(0,5)=='admin'" class="btn btn-primary" @click="download();">下载记录</button> <br><br>
	
	                    <table border="1">
	                        <tr>
	                            <td>设备号</td>
	                            <td>时间</td>
	                            <td>记录备注</td>
	                        </tr>
	                        <tr v-for="(each,index) in res_data2">
	                            <td v-for="(data,index2) in each">
	                                <p v-text="data"></p>
	                            </td>
	                            <!--<td v-text="each[0]"></td>-->
	                        </tr>
	                    </table>
	                </div>
			</center>
	    </div>
	
	
</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello',
			  username: "",
			  intervalId: null,
			  seen_id: 0,
			  seen_table1: 0,
			  //////////////
			  val: [
				  0, 1
			  ],
			  //// 
			  input_val: [null, null, null, null, null, null, null, null], //初始8个null
			  res_data: [],
			  res_data1: [], 
			  res_data2: [], 
			  temperature: "",
			  humidity: "",
			  temptime: "",
			  res_time:"",
			  
			  direction: "http://192.168.137.1:8000"

			}
		},
		onLoad(options) {
			console.log("Op:",options)
			if(options=={}){
			this.username="test";
			}
			else{
			this.username = options.username;		
			}
			//加载时先刷新一下
			this.fresh();
			this.click1();
			
			//定时器
			this.dataRefresh();
		},
		methods: {
			//////////////////////////////////
			    quit(event) {
			          var url = "../index/index"
			          wx.navigateTo({url})
			    },
			    fresh() {
			        console.log("fresh ")
					this.click1();
			    },
			    // 定时刷新数据函数
			    dataRefresh() {
			        // 计时器正在进行中，退出函数
			        if (this.intervalId != null) {
			            return;
			        }
			        // 计时器为空，操作
			        this.intervalId = setInterval(() => {
			            console.log("刷新 " + new Date());
			            this.fresh(); //加载数据函数
			        }, 5000);
			    },
			    // 停止定时器
			    clear() {
			        clearInterval(this.intervalId); //清除计时器
			        this.intervalId = null; //设置为null
			    },
				// //定时器
				// created() {
				// 	this.dataRefresh();
				// },
				destroyed() {
					// 在页面销毁后，清除计时器
					this.clear();
				},
				//////////////////////////////////
				
				//操作--button1
				click1(event) {
					var that = this;
					console.log(event); //可同时获得按钮信息
					// console.log(this.input_val);
					// 提交到后端
					// $.ajaxSettings.async = false; //修改为同步请求！！！
					var param = {
						"kind": "2", //kind=0
						//"data": JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					//http requests
					uni.request({
						url: that.direction + "/test/", 
						data:param,
						header: {'content-type': 'application/x-www-form-urlencoded'},
						method:'GET',//请求方式  或GET，必须为大写
						success: res => {
						console.log('返回', res.data);						
						console.log("get back.")
						that.res_data1 = res.data['data'];
						that.res_time = res.data['time'];
						
						}
					  });
				},
				//操作--button1
				click2(event) {
					that = this;
					console.log(event); //可同时获得按钮信息
					// console.log(this.input_val);
					// 提交到后端
					$.ajaxSettings.async = false; //修改为同步请求！！！
					var param = {
						"kind": "4", //kind=0
						//"data": JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					$.get(that.direction + "/test/", param, function(data, status) {
						console.log("get back.")
						console.log(data);
						that.res_data2 = data['data'];
						that.res_time = data['time'];
						// that.res_show1 = []
						// for (var ii = 0; ii < data['data'][0][2]; ii++) {
						//     if (ii < data['data'][0][1]) {
						//         that.res_show1.push(1);
						//     } else {
						//         that.res_show1.push(0);
						//     }
						// }
					})
				},
				send(a, b, index = 0) {
					console.log("send", a, b);
					that = this;
					console.log(event); //可同时获得按钮信息
					// console.log(this.input_val);
					// 提交到后端
					$.ajaxSettings.async = false; //修改为同步请求！！！
					var param = {
						"kind": "1", //button
						"id": a.toString(),
						"info": b.toString(), //指向 0灯光 1安防 2定时开关 3窗帘
						//"data": JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					console.log(param);
					$.get(that.direction + "/test/", param, function(data, status) {
						console.log("get back.")
						console.log(data);
						that.click1();
						alert("已提交")
					})
				},
				//修改
				change() {
					that = this;
					console.log(event); //可同时获得按钮信息
					// console.log(this.input_val);
					// 提交到后端
					$.ajaxSettings.async = false; //修改为同步请求！！！
					var param = {
						"kind": "3", //kind=0
						"data": JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					$.get(that.direction + "/test/", param, function(data, status) {
						console.log("get back.")
						console.log(data);
						alert("完毕")
					})
				},

				//////////////////////////////////////
				//下载
				download(event) {
				
				that = this; //注意，http请求后的函数中，this的指向为副本的局部，无法真正修改！！所以要用that先复制指针，用that改值
				// 提交到后端
				$.ajaxSettings.async = false; //修改为同步请求！！！
				var param = {
					"kind": "5", //kind=5
					// "parkid": that.input_val[0],
					// "data": JSON.stringify(this.input_val) //数组转json，必须经过此操作！
				}
				console.log(param);

				$.get(that.direction + "/test/", param, function(data, status) {
					console.log(data);
					// 创建隐藏的可下载链接
					var eleLink = document.createElement('a');
					eleLink.download = "temp.txt";
					eleLink.style.display = 'none';
					// 字符内容转变成blob地址
					var blob = new Blob([data]);
					eleLink.href = URL.createObjectURL(blob);
					// 触发点击
					document.body.appendChild(eleLink);
					eleLink.click();
					// 然后移除
					document.body.removeChild(eleLink);
				})
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
