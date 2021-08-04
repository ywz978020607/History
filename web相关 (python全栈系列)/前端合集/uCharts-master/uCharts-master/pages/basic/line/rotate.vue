<template>
	<view class="qiun-columns">
		<!--#ifdef H5 -->
		<view class="qiun-bg-white qiun-title-bar qiun-common-mt" >
			<view class="qiun-title-dot-light">页面地址</view>
		</view>
		<view class="qiun-bg-white qiun-padding">
		    <text>pages/basic/line/rotate</text>
		</view>
		<!--#endif-->
		<view class="qiun-bg-white qiun-title-bar qiun-common-mt" >
			<view class="qiun-title-dot-light">横屏模式带滚动条</view>
		</view>
		<view class="qiun-charts-rotate" >
			<!--#ifdef MP-ALIPAY -->
			<canvas canvas-id="canvasLineB" id="canvasLineB" class="charts-rotate" :style="{'width':cWidth2*pixelRatio+'px','height':cHeight2*pixelRatio+'px', 'transform': 'scale('+(1/pixelRatio)+')','margin-left':-cWidth2*(pixelRatio-1)/2+'px','margin-top':-cHeight2*(pixelRatio-1)/2+'px'}" @touchstart="touchLineB" @touchmove="moveLineB" @touchend="touchEndLineB"></canvas>
			<!--#endif-->
			<!--#ifndef MP-ALIPAY -->
			<canvas canvas-id="canvasLineB" id="canvasLineB" class="charts-rotate" @touchstart="touchLineB" @touchmove="moveLineB" @touchend="touchEndLineB"></canvas>
			<!--#endif-->
		</view>
		<!--#ifdef H5 -->
		<view class="qiun-bg-white qiun-title-bar qiun-common-mt" >
			<view class="qiun-title-dot-light">标准数据格式</view>
		</view>
		<view class="qiun-bg-white qiun-padding">
		    <textarea class="qiun-textarea" auto-height="true" maxlength="-1" v-model="textarea"/>
		</view>
		<view class="qiun-text-tips">Tips：修改后点击更新图表</view>
		<button class="qiun-button" @tap="changeData()">更新图表</button>
		<!--#endif-->
	</view>
</template>

<script>
	import uCharts from '@/components/u-charts/u-charts.js';
	import  { isJSON } from '@/common/checker.js';
	var _self;
	var canvaLineB=null;
	
	export default {
		data() {
			return {
				cWidth2:'',//横屏图表
				cHeight2:'',//横屏图表
				pixelRatio:1,
				textarea:''
			}
		},
		onLoad() {
			_self = this;
			//#ifdef MP-ALIPAY
			uni.getSystemInfo({
				success: function (res) {
					if(res.pixelRatio>1){
						//正常这里给2就行，如果pixelRatio=3性能会降低一点
						//_self.pixelRatio =res.pixelRatio;
						_self.pixelRatio =2;
					}
				}
			});
			//#endif
			this.cWidth2=uni.upx2px(700);
			this.cHeight2=uni.upx2px(1100);
			this.getServerData();
		},
		methods: {
			getServerData(){
				uni.request({
					url: 'https://www.easy-mock.com/mock/5cc586b64fc5576cba3d647b/uni-wx-charts/chartsdata2',
					data:{
					},
					success: function(res) {
						console.log(res.data.data)
						let LineB={categories:[],series:[]};
						//这里我后台返回的是数组，所以用等于，如果您后台返回的是单条数据，需要push进去
						LineB.categories=res.data.data.LineB.categories;
						LineB.series=res.data.data.LineB.series;
						_self.textarea = JSON.stringify(res.data.data.LineB);
						_self.showLineB("canvasLineB",LineB);
					},
					fail: () => {
						_self.tips="网络错误，小程序端请检查合法域名";
					},
				});
			},
			showLineB(canvasId,chartData){
				canvaLineB=new uCharts({
					$this:_self,
					canvasId: canvasId,
					type: 'line',
					fontSize:11,
					legend:true,
					background:'#FFFFFF',
					pixelRatio:_self.pixelRatio,
					rotate:true,//开启图表横屏
					// #ifdef MP-ALIPAY || MP-BAIDU
					rotateLock:true,//百度及支付宝需要锁定旋转
					// #endif
					categories: chartData.categories,
					enableScroll: true,//开启图表拖拽功能
					animation: false,
					series: chartData.series,
					xAxis: {
						disableGrid:false,
						type:'grid',
						gridType:'dash',
						itemCount:4,//可不填写，配合enableScroll图表拖拽功能使用，x轴单屏显示数据的数量，默认为5个
						scrollShow:true,//新增是否显示滚动条，默认false
						scrollAlign:'left',
						//scrollBackgroundColor:'#F7F7FF',//可不填写，配合enableScroll图表拖拽功能使用，X轴滚动条背景颜色,默认为 #EFEBEF
						//scrollColor:'#DEE7F7',//可不填写，配合enableScroll图表拖拽功能使用，X轴滚动条颜色,默认为 #A6A6A6
					},
					yAxis: {
						//disabled:true
					},
					width: _self.cWidth2*_self.pixelRatio,
					height: _self.cHeight2*_self.pixelRatio,
					dataLabel: true,
					dataPointShape: true,
					extra: {
						line:{
							type: 'curve'
						}
					},
				});
			},
			touchLineB(e){
				canvaLineB.scrollStart(e);
			},
			moveLineB(e) {
				canvaLineB.scroll(e);
			},
			touchEndLineB(e) {
				canvaLineB.scrollEnd(e);
				//下面是toolTip事件，如果滚动后不需要显示，可不填写
				canvaLineB.showToolTip(e, {
					format: function (item, category) {
						return category + ' ' + item.name + ':' + item.data 
					}
				});
			},
			changeData(){
				if(isJSON(_self.textarea)){
					let newdata=JSON.parse(_self.textarea);
					canvaLineB.updateData({
						series: newdata.series,
						categories: newdata.categories
					});
				}else{
					uni.showToast({
						title:'数据格式错误',
						image:'../../../static/images/alert-warning.png'
					})
				}
			}
		}
	}
</script>

<style>
	/*样式的width和height一定要与定义的cWidth和cHeight相对应*/
	.qiun-charts-rotate {
		width: 700upx;
		height: 1100upx;
		background-color: #FFFFFF;
		padding: 25upx;
	}
	
	.charts-rotate {
		width: 700upx;
		height: 1100upx;
		background-color: #FFFFFF;
	}
</style>
