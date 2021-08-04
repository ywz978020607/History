<template>
	<view class="qiun-columns">
		<view class="qiun-bg-white qiun-title-bar qiun-common-mt" >
			<view class="qiun-title-dot-light">饼图右侧图例</view>
		</view>
		<view class="qiun-charts qiun-rows" >
			<canvas canvas-id="canvasPie" id="canvasPie" class="charts-pie" @touchstart="touchPie"></canvas>
			<view class="qiun-bg-white charts-right">
				<view>
					<block v-for="(item, index) in piearr" :key="index">
						<view class="qiun-rows legend-itme">
							<view class="legend-itme-point" :style="{'background-color':item.color}"></view>
							<view class="legend-itme-text">{{item.name}}:{{item.data}}人</view>
						</view>
					</block>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import uCharts from '@/components/u-charts/u-charts.js';
	var _self;
	var canvaPie=null;
	/*下面是服务器返回的数据格式
	var Data={
			"Pie": {
			  "series": [{
				"name": "一班",
				"data": 50
			  }, {
				"name": "二班",
				"data": 30
			  }, {
				"name": "三班",
				"data": 20
			  }, {
				"name": "四班",
				"data": 18
			  }, {
				"name": "五班",
				"data": 8
			  }]
			}
		}
	*/
   
	export default {
		data() {
			return {
				cWidth:'',
				cHeight:'',
				pixelRatio:1,
				serverData:'',
				piearr:[]
			}
		},
		onLoad() {
			_self = this;
			this.cWidth=uni.upx2px(500);
			this.cHeight=uni.upx2px(540);
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
						let Pie={series:[]};
						//这里我后台返回的是数组，所以用等于，如果您后台返回的是单条数据，需要push进去
						Pie.series=res.data.data.Pie.series;
						_self.showPie("canvasPie",Pie);
					},
					fail: () => {
						_self.tips="网络错误，小程序端请检查合法域名";
					},
				});
			},
			showPie(canvasId,chartData){
				canvaPie=new uCharts({
					$this:_self,
					canvasId: canvasId,
					type: 'pie',
					fontSize:11,
					legend:false,
					background:'#FFFFFF',
					pixelRatio:_self.pixelRatio,
					series: chartData.series,
					animation: true,
					width: _self.cWidth*_self.pixelRatio,
					height: _self.cHeight*_self.pixelRatio,
					dataLabel: true,
					extra: {
						pie: {
						  lableWidth:15
						}
					},
				});
				this.piearr=canvaPie.opts.series;
			},
			touchPie(e){
				canvaPie.showToolTip(e, {
					format: function (item) {
						return item.name + ':' + item.data 
					}
				});
			},
		}
	}
</script>

<style>
page{background:#F2F2F2;width: 750upx;overflow-x: hidden;}
.qiun-padding{padding:2%; width:96%;}
.qiun-wrap{display:flex; flex-wrap:wrap;}
.qiun-rows{display:flex; flex-direction:row !important;}
.qiun-columns{display:flex; flex-direction:column !important;}
.qiun-common-mt{margin-top:10upx;}
.qiun-bg-white{background:#FFFFFF;}
.qiun-title-bar{width:96%; padding:10upx 2%; flex-wrap:nowrap;}
.qiun-title-dot-light{border-left: 10upx solid #0ea391; padding-left: 10upx; font-size: 32upx;color: #000000}
.qiun-charts{width: 750upx; height:500upx;background-color: #FFFFFF;}
.charts-pie{width: 550upx; height:500upx;background-color: #FFFFFF;}
.charts-right{display:flex;align-items:center;width: 250upx; height:500upx;background-color: #FFFFFF;}
.legend-itme{width: 200upx; margin-left: 30upx; height:50upx;align-items:center;}
.legend-itme-point{width: 20upx; height:20upx; margin: 15upx;  border: 1px solid #FFFFFF; border-radius: 20upx;background-color: #000000;}
.legend-itme-text{height:50upx;line-height: 50upx;color: #666666;font-size: 26upx;}
</style>
