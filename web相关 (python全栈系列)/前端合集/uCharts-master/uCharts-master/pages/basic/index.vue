<template>
	<view>
		<uni-swiper-dot :info="info" :current="current" field="content" mode="nav" >
			<swiper class="swiper-box" @change="change">
				<swiper-item v-for="(item ,index) in info" :key="index">
						<image :src="item.images" class="swiper-item"></image>
				</swiper-item>
			</swiper>
		</uni-swiper-dot>
		<uni-notice-bar show-icon="true" scrollable="true" single="true" :text="notice" speed=50>
		</uni-notice-bar>
		<uni-grid :options="options" column-num="4">
		</uni-grid>
	</view>
</template>

<script>
import uniSwiperDot from "@/components/uni-ui/uni-swiper-dot/uni-swiper-dot.vue";
import uniNoticeBar from "@/components/uni-ui/uni-notice-bar/uni-notice-bar.vue";
import uniGrid from "@/components/uni-ui/uni-grid/uni-grid.vue";

export default {
	components: {
		uniSwiperDot,
		uniNoticeBar,
		uniGrid
	},
	data() {
		return {
			info: [{
                content: 'uCharts跨全端图表,支持H5、APP、小程序',
				images:'../../static/images/banner/banner1.png'
            }, {
                content: 'uCharts荣获uni-app插件大赛一等奖',
				images:'../../static/images/banner/banner2.png'
            }],
            current: 0,
			notice:'uCharts跨全端图表，荣获插件大赛一等奖，感谢DCloud以及mpvue团队的鼓励和认可！感谢各位开发者的问题反馈和赞赏！',
			options:[
			{image:'../../static/images/charts/column-group.png',text:'柱状图',url:'column/column'},
			{image:'../../static/images/charts/column-stack.png',text:'堆叠图',url:'column/stack'},
			{image:'../../static/images/charts/column-meter.png',text:'温度计',url:'column/meter'},
			{image:'../../static/images/charts/bar-group.png',text:'横屏模式',url:'column/rotate'},
			{image:'../../static/images/charts/line.png',text:'折线图',url:'line/line'},
			{image:'../../static/images/charts/line-curve.png',text:'曲线图',url:'line/curve'},
			{image:'../../static/images/charts/line-scroll.png',text:'滚动条',url:'line/line-scroll'},
			{image:'../../static/images/charts/line-rotate.png',text:'横屏模式',url:'line/rotate'},
			{image:'../../static/images/charts/pie.png',text:'饼图',url:'pie/pie'},
			{image:'../../static/images/charts/ring.png',text:'圆环图',url:'pie/ring'},
			{image:'../../static/images/charts/rose.png',text:'玫瑰图',url:'pie/rose'},
			{image:'../../static/images/charts/arc-bar.png',text:'进度条',url:'arcbar/arcbar'},
			{image:'../../static/images/charts/area2.png',text:'区域图',url:'area/area'},
			{image:'../../static/images/charts/mix.png',text:'混合图',url:'mix/mix'},
			{image:'../../static/images/charts/candle.png',text:'K线图',url:'candle/candle'},
			{image:'../../static/images/charts/gauge.png',text:'仪表盘',url:'gauge/gauge'},
			{image:'../../static/images/charts/radar.png',text:'雷达图',url:'radar/radar'}]
		};
	},
	methods: {
        change(e) {
            this.current = e.detail.current;
        }
    }
};
</script>

<style>
.swiper-box{width: 750upx;height: 400upx;}
.swiper-item{width: 750upx;height: 400upx;}
</style>
