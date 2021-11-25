<template>
	<div style="display: flex;flex-direction: column;align-items: center;">
	        <header id="top">
	            <!-- 内容显示区域 ：width : 1211px -->
	            <div id="top_box">
	                <!--<ul class="lf">
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
	<div style="display: flex;flex-direction: column;align-items: center;">
		            <br> <br>
					
					<span style="white-space: nowrap;">
		                <button class="btn btn-primary" @click="seen_id=0">查询系统</button> <span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;'"></span>
						<button  class="btn btn-primary" @click="seen_id=1;">修改信息</button> <span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;'"></span>
						<button v-if="username=='admin'" class="btn btn-primary" @click="seen_id=2; buttonadmin();">用户管理 </button><span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;'"></span>
						<!--<button  class="btn btn-primary" @click="seen_id=3;getandshow();">曲线图查看</button> -->
						</span>
						<!--v-if="username.slice(0,5)=='admin'"-->
						<br> <br> <br>
						<div v-if="seen_id==0" style="display: flex;flex-direction: column;align-items: center;">
							<h2>查询系统</h2>
							<p>当前时间{{res_time}}</p>
					
							<hr style="width: 100%; size: 3em;" />
							<div v-for="(each,index) in res_data1['data']" style="display: flex;flex-direction: column;align-items: center;">
								<p>备注: {{each[9]}} </p>
								<p>设备号: {{each[0]}} <span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;'"></span> <button @click="deleteproduct(each[0]);">删除该设备</button></p>
								<p>报警邮箱: {{each[6]}} </p>
								<p>更新时间: {{each[1].slice(0,10)+' ' +each[1].slice(11,19)}}</p>
								
								<canvas :canvas-id=canvasnamelist[index]  class="charts" :style="{'width':cWidth*1+'px','height':cHeight*2+'px', 'transform': 'scale('+(1/4)+')','margin-left':-cWidth*(1)/2+'px','margin-top':-cWidth*(1)/4+'px','margin-bottom':-cWidth*(1)/6+'px'}" ></canvas>
								
								<p>温度数值: {{each[2]}} <span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;'"></span> 温度阈值: {{each[3]}}</p>
								<p>
									<span v-if="each[4]==-1">温度报警：关闭&nbsp;&nbsp;&nbsp;&nbsp; </span>
									<span v-else-if="each[4]==0">温度报警：正常&nbsp;&nbsp;&nbsp;&nbsp; </span>
									<span v-else>温度报警：报警&nbsp;&nbsp;&nbsp;&nbsp; 时间：{{each[5].slice(0,10)+' ' +each[5].slice(11,19)}}</span>
									</p>
									<p>
									<button v-if="each[4]==-1" class="btn btn-primary" @click="send(each[0],1,each[7])">温度报警部署</button>
									<button v-else class="btn btn-primary" @click="send(each[0],1,each[7])">温度报警解除</button> &nbsp;&nbsp;&nbsp;&nbsp;
								</p>
								
								<hr style="width: 35%; size: 3em;" />
								<p>
								<span v-if="each[8]==0 | each[8]==2">控制器: 关闭 <br> <button class="btn btn-primary" @click="send(each[0],0,each[7])">手动开启</button></span>
								<span v-else>控制器: 开启 <br> <button class="btn btn-primary" @click="send(each[0],0,each[7])">手动关闭</button></span>
								<span v-if="each[8]==2 | each[8]==3"><br> <button class="btn btn-primary" @click="send(each[0],'00',each[7])">切回自动</button></span>
								</p>
								<br>
								
								<hr style="width: 100%; size: 3em;" />
							</div>
		
						</div>
		
						<div v-if="seen_id==1" style="display: inline-block;">
							<label style="float:left">设备产品ID：</label> <input v-model="input_val[0]" style="border:0.5px solid #378888; white-space: nowrap;">
							<br>
							<label style="float:left">通知邮箱：</label> <input v-model="input_val[1]" style="border:0.5px solid #378888; white-space: nowrap;">
							<br>
							<label style="float:left">温度阈值：</label> <input v-model="input_val[2]" style="border:0.5px solid #378888; white-space: nowrap;">
							<br>
							<label style="float:left">密钥：</label> <input v-model="input_val[3]" style="border:0.5px solid #378888; white-space: nowrap;">
							<br>
							<label style="float:left">备注：</label> <input v-model="input_val[4]" style="border:0.5px solid #378888; white-space: nowrap;">
							<br>
							<br><br>
		
							<button class="btn btn-primary" @click="change" style="display: flex;flex-direction: column;align-items: center;">新增/修改</button>
						</div>
		
		
						<div v-if="seen_id==2" style="display: flex;flex-direction: column;align-items: center;">
							<h2>账号管理</h2>
							
							<span style="white-space: nowrap;"><label style="float:left">账号：</label> <input v-model="input_val[0]"><br></span>
							<span style="white-space: nowrap;"><label style="float:left">新密码：</label> <input v-model="input_val[1]"><br></span>
							
							<span style="white-space: nowrap;"><button class="btn btn-primary" @click="changeadmin();buttonadmin();">修改</button> <span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;'"></span>
							<button class="btn btn-primary" @click="registeradmin();buttonadmin();">注册</button>
							</span>
							<hr style="width: 55%; size: 3em;" />

							<h2>查询</h2>
							<scroll-view class=" mx-4 border align-center" style="width: 700upx;height: 600upx; white-space: nowrap" scroll-x="true" scroll-y="true" >
							<table class=" mx-4 border align-center" border="1">
								<tr>
									<td>账户</td>
									<td>密码</td>
									<td>操作</td>
								</tr>
								<tr v-for="(each,index) in res_data_admin">
									<!--<td v-for="(data,index2) in each">
										<p v-text="data"></p>
									</td>-->
									<td v-text="each[0]"></td>
									<td v-text="each[1]"></td>
									<td><button class="btn btn-primary " @click="deleteadmin(each[0]);buttonadmin();">删除用户</button></td>
								</tr>
								
							</table>
							</scroll-view>
							<br>
							<button class="btn btn-primary " @click="buttonadmin ">查询</button>
							<br><br>
						</div>
		                		
		                <div v-if="seen_id==3" style="display: flex;flex-direction: column;align-items: center;">
		                    <p>当前时间{{res_time}}</p>
		                    <br>
		                    <h2>查询系统</h2>
							<br>
							<!-- <input id="input1"></input> -->
							<span style="white-space: nowrap;">
							<span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;'"></span>{{temp_index+1}}/{{parseInt(all_count/charts_len-1)+1}}页<span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;'"></span><button id="btn1" class="btn btn-primary" @click="click_jump">到达</button>
							<input v-model="input_val[0]" style="border:0.5px solid #378888; white-space: nowrap;" /> 
							</span>
							<span style="white-space: nowrap;"><button id="btn1" class="btn btn-primary" @click="click_last()">上一页</button><span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;'"></span><button id="btn1" class="btn btn-primary" @click="click_next()">下一页</button></span>
							<br>
		                    <br>
							
		                    <div style="display: flex;flex-direction: column;align-items: center;">
								空气温度历史曲线
								<canvas canvas-id="canvasLineA" id="canvasLineA" class="charts"></canvas>
								<br>
								空气湿度历史曲线
								<canvas canvas-id="canvasLineB" id="canvasLineB" class="charts"></canvas>
								<br>
								土壤温度历史曲线
								<canvas canvas-id="canvasLineC" id="canvasLineC" class="charts"></canvas>
								<br>
								土壤湿度历史曲线
								<canvas canvas-id="canvasLineD" id="canvasLineD" class="charts"></canvas>
								光照数值历史曲线
								<canvas canvas-id="canvasLineE" id="canvasLineE" class="charts"></canvas>
				
		                        <br><br>
		                        <button class="btn btn-primary" @click="getandshow()">查询</button>
		                    </div>
		
		                </div>
	
				</div>
				
					
	    </div>
	
	
</template>

<script>
	import uCharts from '@/static/u-charts/u-charts.js';
	import wxCharts from '@/static/wxcharts.js'; //@=../..
	var _self;
	var canvaGauge=null; //必须！否则报错
	
		var _self;
		var canvaLineA=null;
		//这里的Data为测试使用，生产环境请从服务器获取
		var Data={
			LineA:{categories:['2012', '2013', '2014', '2015', '2016', '2017'],series:[{name: '成交量A',data:[35, 20, 25, 37, 4, 20]},{name: '成交量B',data:[70, 40, 65, 100, 44, 68]},{name: '成交量C',data:[100, 80, 95, 150, 112, 132]},{name: '成交量D',data:[100, 80, 95, 150, 112, 132]}]},
			Line1:{categories:['2012', '2013', '2014', '2015', '2016', '2017'],series:[{name: '空气温度',data:[35, 20, 25, 37, 4, 20]}]},
			Line2:{categories:['2012', '2013', '2014', '2015', '2016', '2017'],series:[{name: '空气湿度',data:[35, 20, 25, 37, 4, 20]}]},
			Line3:{categories:['2012', '2013', '2014', '2015', '2016', '2017'],series:[{name: '土壤温度',data:[35, 20, 25, 37, 4, 20]}]},
			Line4:{categories:['2012', '2013', '2014', '2015', '2016', '2017'],series:[{name: '土壤湿度',data:[35, 20, 25, 37, 4, 20]}]},
			Line5:{categories:['2012', '2013', '2014', '2015', '2016', '2017'],series:[{name: '光照数值',data:[35, 20, 25, 37, 4, 20]}]},
			
			}
			
	export default {
		data() {
			return {
				canvasnamelist:["canvasGauge0","canvasGauge1"],
				title: 'Hello',
			  username: "",
			  intervalId: null,
			  seen_id: 0,
			  seen_table1: 0,
			  //////////////
			  val: [
				  0, 1
			  ],
			  ///画图变量
			  cWidth:'',
			cHeight:'',
			pixelRatio:1,
			  //翻页变量
			  temp_index: 0,
			  all_count: null,
			  charts_len: 7,
			  //// 
			  //// 
			  input_val: [null, null, null, null, null, null, null, null], //初始8个null
			  res_data: [],
			  res_data1: [], 
			  res_data2: [], 
			  temperature: "",
			  humidity: "",
			  temptime: "",
			  res_time:"",
			  res_data_admin: [],
			  
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
			
			//画布
			_self = this;
			//#ifdef H5 || MP-ALIPAY || MP-BAIDU || MP-TOUTIAO
			uni.getSystemInfo({
				success: function (res) {
					if(res.pixelRatio>1){
						_self.pixelRatio =2;
						//正常这里_self.pixelRatio给2就行，如果要求高可用下行
						//_self.pixelRatio =res.pixelRatio;
					}
				}
			});
			//#endif
			this.cWidth=uni.upx2px(750);
			this.cHeight=uni.upx2px(500);
		},
		onReady() {
			;
			// this.showLineA("canvasLineA",Data.LineA);
				},
		methods: {
			//////////////////////////////////
			    quit(event) {
			          var url = "../index/index"
			          wx.navigateTo({url})
			    },
				draw(){
					this.showLineA("canvasLineA",Data.LineA);
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
				///
				//admin
				buttonadmin() {
					var that = this;
					// 提交到后端
					// $.ajaxSettings.async = false; //修改为同步请求！！！
					var param = {
						"kind": "000", //kind=0
						// "data": JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					uni.request({
						url: that.direction + "/test/", 
						data:param,
						header: {'content-type': 'application/x-www-form-urlencoded'},
						method:'GET',//请求方式  或GET，必须为大写
						success: res => {
						console.log("get back.")
						console.log(res.data);
						that.res_data_admin = res.data['data'];
						}
					  });
					  
				},
				deleteadmin(data) {
					var that = this;
					console.log(data);
					var param = {
						"kind": "001", //kind=0
						"name": data, //JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					uni.request({
						url: that.direction + "/test/", 
						data:param,
						header: {'content-type': 'application/x-www-form-urlencoded'},
						method:'GET',//请求方式  或GET，必须为大写
						success: res => {
						console.log("get back.")
						console.log(res.data);
						if (res.data['status'] == 'ok') {
							uni.showToast({
							    title: "成功",
							    icon: "none"
							})
						} else {
							uni.showToast({
							    title: "失败",
							    icon: "none"
							})
						}
						
						}
					  });
					  
				},
				changeadmin() {
					var that = this;
					// console.log(data);
					var param = {
						"kind": "002", //kind=0
						"name": this.input_val[0], //JSON.stringify(this.input_val) //数组转json，必须经过此操作！
						"newpasswd": this.input_val[1] //JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					uni.request({
						url: that.direction + "/test/", 
						data:param,
						header: {'content-type': 'application/x-www-form-urlencoded'},
						method:'GET',//请求方式  或GET，必须为大写
						success: res => {
						console.log("get back.")
						console.log(res.data);
						if (res.data['status'] == 'ok') {
							uni.showToast({
							    title: "成功",
							    icon: "none"
							})
						} else {
							uni.showToast({
							    title: "失败",
							    icon: "none"
							})
						}
						
						}
					  });
					  
				},
				registeradmin() {
					var that = this;
					// console.log(data);
					var param = {
						"kind": "003", //kind=0
						"name": this.input_val[0], //JSON.stringify(this.input_val) //数组转json，必须经过此操作！
						"newpasswd": this.input_val[1] //JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					uni.request({
						url: that.direction + "/test/", 
						data:param,
						header: {'content-type': 'application/x-www-form-urlencoded'},
						method:'GET',//请求方式  或GET，必须为大写
						success: res => {
						console.log("get back.")
						console.log(res.data);
						if (res.data['status'] == 'ok') {
							uni.showToast({
							    title: "成功",
							    icon: "none"
							})
						} else {
							uni.showToast({
							    title: "失败",
							    icon: "none"
							})
						}
						
						}
					  });
					  
				},
				//////////////////////
				deleteproduct(data) {
					var that = this;
					console.log(data);
					var param = {
						"kind": "31", //kind=0
						"username":that.username,
						"id": data, //JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					uni.request({
						url: that.direction + "/test/", 
						data:param,
						header: {'content-type': 'application/x-www-form-urlencoded'},
						method:'GET',//请求方式  或GET，必须为大写
						success: res => {
						console.log("get back.")
						console.log(res.data);
						if (res.data['status'] == 'ok') {
							uni.showToast({
							    title: "成功",
							    icon: "none"
							})
							that.click1();
						} else {
							uni.showToast({
							    title: "失败",
							    icon: "none"
							})
						}
						
						}
					  });
					  
				},
				//操作--button1
				click1(event) {
					var that = this;
					// console.log(event); //可同时获得按钮信息
					// console.log(this.input_val);
					// 提交到后端
					// $.ajaxSettings.async = false; //修改为同步请求！！！
					var param = {
						"kind": "2", //kind=0
						"username":that.username,
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
						that.res_data1 = res.data;
						that.res_time = res.data['time'];
						
						console.log("length");
						console.log(res.data.data.length);
						
						
						for(var ii=0;ii<res.data.data.length ;ii++){
							console.log(ii);
							that.canvasnamelist[ii] = "canvasGauge"+ii.toString();
							let val = parseFloat(res.data.data[ii][2]);
							console.log(val);
							let Gauge={"categories":[{"value":0.2,"color":"#1890ff"},{"value":0.8,"color":"#2fc25b"},{"value":1,"color":"#f04864"}],
							"series":[{"name":"温度","data":val/100,"ori":val}]}; //如果最大温度是100的话
							
							this.showGauge(that.canvasnamelist[ii],Gauge);
							// this.showGauge("canvasGauge0",Gauge);	
						}
						
						
						}
					  });
				},
				send(a, b, passwd) {
					console.log("send", a, b);
					var that = this;
					// console.log(event); //可同时获得按钮信息
					// console.log(this.input_val);
					// 提交到后端
					// $.ajaxSettings.async = false; //修改为同步请求！！！
					var param = {
						"kind": "1", //button
						"id": a.toString(),
						"info": b.toString(), //指向
						"password":passwd,
						//"data": JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					// console.log(param);
					// $.get(that.direction + "/test/", param, function(data, status) {
					// 	console.log("get back.")
					// 	console.log(data);
					// 	that.click1();
					// 	alert("已提交")
					// })
					
					//http requests
					uni.request({
						url: that.direction + "/test/", 
						data:param,
						header: {'content-type': 'application/x-www-form-urlencoded'},
						method:'GET',//请求方式  或GET，必须为大写
						success: res => {
						console.log('返回', res.data);		
						that.click1();
						uni.showToast({
						    title: "完毕",
						    icon: "none"
						})
						}
					  });
				},
				//修改
				change(event) {
					var that = this;
					console.log(event); //可同时获得按钮信息
					// console.log(this.input_val);
					// 提交到后端
					// $.ajaxSettings.async = false; //修改为同步请求！！！
					var param = {
						"kind": "3", //kind=0
						"username":that.username,
						"data": JSON.stringify(this.input_val) //数组转json，必须经过此操作！
					}
					// $.get(that.direction + "/test/", param, function(data, status) {
					// 	console.log("get back.")
					// 	console.log(data);
					// 	alert("完毕")
					// })
					//http requests
					uni.request({
						url: that.direction + "/test/", 
						data:param,
						header: {'content-type': 'application/x-www-form-urlencoded'},
						method:'GET',//请求方式  或GET，必须为大写
						success: res => {
						console.log('返回', res.data);	
						if(res.data['status']=='fail'){
							uni.showToast({
								title: "设备号/密钥不正确",
								icon: "none"
							})								
						}
						else{
							uni.showToast({
								title: "完毕",
								icon: "none"
							})	
						}
						
						}
					  });
				},
				//gauge
				showGauge(canvasId,chartData){
					canvaGauge = new uCharts({
						$this:_self,
						canvasId: canvasId,
						type: 'gauge',
						fontSize:11,
						legend:false,
						title: {
							name: (chartData.series[0].ori)+'℃', //Math.round()
							color: chartData.categories[1].color,
							fontSize: 25*_self.pixelRatio,
							offsetY:50*_self.pixelRatio,//新增参数，自定义调整Y轴文案距离
						},
						subtitle: {
							name: chartData.series[0].name,
							color: '#666666',
							fontSize: 15*_self.pixelRatio,
							offsetY:-50*_self.pixelRatio,//新增参数，自定义调整Y轴文案距离
						},
						extra: {
							gauge:{
								type:'default',
								width: _self.gaugeWidth*_self.pixelRatio,//仪表盘背景的宽度
								startAngle:0.75,
								endAngle:0.25,
								startNumber:0.0,
								endNumber:100.0,
								splitLine:{
									fixRadius:0,
									splitNumber:10,
									width: _self.gaugeWidth*_self.pixelRatio,//仪表盘背景的宽度
									color:'#FFFFFF',
									childNumber:5,
									childWidth:_self.gaugeWidth*0.4*_self.pixelRatio,//仪表盘背景的宽度
								},
								pointer:{
									width: _self.gaugeWidth*0.8*_self.pixelRatio,//指针宽度
									color:'auto'
								}
							}
						},
						background:'#FFFFFF',
						pixelRatio:_self.pixelRatio,
						categories: chartData.categories,
						series: chartData.series,
						animation: false,
						width: _self.cWidth*_self.pixelRatio*1/2,
						height: _self.cHeight*_self.pixelRatio,
						dataLabel: true,
					});
				},
				
				//curve
				//////////////////////////////////////
				getandshow(event){
					var that = this;
					console.log(event); //可同时获得按钮信息
					// console.log(this.input_val);
					// 提交到后端
					// $.ajaxSettings.async = false; //修改为同步请求！！！
					var param = {
						"username":that.username,
						"kind": "4", //kind=0
						"temp_index": that.temp_index,
						"charts_len": that.charts_len,
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
						// that.res_data1 = res.data['data'];
						// that.res_time = res.data['time'];
						
						that.all_count = (res.data["all_count"]);
						for (var i = 0; i < that.charts_len; i++) {
							Data.Line1.series[0].data[i] = parseFloat(res.data[i]['data'][0]);
							Data.Line2.series[0].data[i] = parseFloat(res.data[i]['data'][1]);
							Data.Line3.series[0].data[i] = parseFloat(res.data[i]['data'][2]);
							Data.Line4.series[0].data[i] = parseFloat(res.data[i]['data'][3]);
							Data.Line5.series[0].data[i] = parseFloat(res.data[i]['data'][4]);
							
							Data.Line1.categories[i] = res.data[i]['time']; //data['datastreams'][4]['datapoints'].slice(-charts_len)[i]['at'].slice(5,19);
							Data.Line2.categories[i] = res.data[i]['time']; //data['datastreams'][4]['datapoints'].slice(-charts_len)[i]['at'].slice(5,19);
							Data.Line3.categories[i] = res.data[i]['time']; //data['datastreams'][4]['datapoints'].slice(-charts_len)[i]['at'].slice(5,19);
							Data.Line4.categories[i] = res.data[i]['time']; //data['datastreams'][4]['datapoints'].slice(-charts_len)[i]['at'].slice(5,19);
							Data.Line5.categories[i] = res.data[i]['time']; //data['datastreams'][4]['datapoints'].slice(-charts_len)[i]['at'].slice(5,19);
							//console.log(my_data[1][i]);
						}
						this.changeData();
						
						}
					  });
				},
				
				showLineA(canvasId,chartData){
					var pixelRatio=0.9;
					canvaLineA=new wxCharts({
						canvasId: canvasId,
						type: 'line',
						fontSize:10,
						legend:true,
						background:'#FFFFFF',
						pixelRatio:pixelRatio,//_self.pixelRatio,
						categories: chartData.categories,
						series: chartData.series,
						animation: false,
						enableScroll: false,//true,//开启图表拖拽功能
						xAxis: {
							disableGrid:true,
							itemCount:this.charts_len,//可不填写，配合enableScroll图表拖拽功能使用，x轴单屏显示数据的数量，默认为5个
							//scrollBackgroundColor:'#F7F7FF',//可不填写，配合enableScroll图表拖拽功能使用，X轴滚动条背景颜色,默认为 #EFEBEF
							//scrollColor:'#DEE7F7',//可不填写，配合enableScroll图表拖拽功能使用，X轴滚动条颜色,默认为 #A6A6A6
						},
						yAxis: {
							type:'value',
							axisLabel:{
								margin:uni.upx2px(400),
								show:true,
								interval: 'auto',
							},
							//disabled:true
						},
						grid:{
							left:450,
						},
						width: _self.cWidth*pixelRatio,//_self.pixelRatio,
						height: _self.cHeight*pixelRatio,//_self.pixelRatio,
						dataLabel: false, //显示数值与否
						dataPointShape: true,
						extra: {
							lineStyle: 'straight'
						},
					});
					// alert(_self.cWidth);
					// alert(_self.cHeight);
					// alert(_self.pixelRatio);
				},
				changeData(){
					//这里只做了柱状图数据动态更新，其他图表同理。
					// canvaLineA.updateData({
					// 	series: Data.Line1.series,
					// 	categories: Data.Line1.categories
					// });
					this.showLineA("canvasLineA",Data.Line1);
					this.showLineA("canvasLineB",Data.Line2);
					this.showLineA("canvasLineC",Data.Line3);
					this.showLineA("canvasLineD",Data.Line4);
					this.showLineA("canvasLineE",Data.Line5);
				},
				
				//翻页按键
				//按键
				click_last(event) {
					this.temp_index -= 1;
					if (this.temp_index < 0) {
						this.temp_index = 0;
						// alert("已到头")
						uni.showToast({
						    title: "已到头",
						    icon: "none"
						})
					}
					this.getandshow();
				},
				//按键
				click_next(event) {
					if (this.temp_index >= parseInt(this.all_count / this.charts_len) - 1) {
						// alert("已到头")
						uni.showToast({
						    title: "已到头",
						    icon: "none"
						})
					} else {
						this.temp_index += 1;
					}
					this.getandshow();
				},
				//按键
				click_jump(event) {
					this.temp_index = parseInt(this.input_val[0]) - 1; //显示和传输差1
					console.log(this.temp_index);
					if (this.temp_index < 0) {
						this.temp_index = 0;
					}
					if (this.temp_index >= parseInt(this.all_count / this.charts_len) - 1) {
						this.temp_index = parseInt(this.all_count / this.charts_len) - 1
					}
					console.log(this.temp_index);
					this.getandshow();
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
	
	
	/* .charts{width: 750upx; height:500upx;background-color: #FFFFFF;} */
	.charts{width: 750upx; height:500upx;background-color: #FFFFFF;}
</style>
