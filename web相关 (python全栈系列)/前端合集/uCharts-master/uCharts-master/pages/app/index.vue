<template>
	<view>
		<block v-for="(item ,index) in info" :key="index">
			<uni-card :title="item.title" :thumbnail="'../../static/images/charts/'+item.images" bgcolor='#f7f7fa' :images="item.demo" :note="'Tips:'+item.tips" @click="clickCard(item.url)">
			</uni-card>
		</block>
	</view>
</template>

<script>
	import uniCard from '@/components/uni-ui/uni-card/uni-card.vue'
	export default {
		data() {
			return {
				info: [{
				    title: 'K线图与柱状图联动',
					images:'candle.png',
					url:'demo/candle',
					demo:'../../static/images/demo/demo3.png',
					tips:'更新中'
				},{
				    title: '单页多图表好性能',
					images:'mix2.png',
					url:'demo/index',
					demo:'../../static/images/demo/demo2.png',
					tips:'点击查看示例'
				},{
				    title: '饼图右侧图例',
					images:'pie.png',
					url:'demo/pie-legend',
					demo:'../../static/images/demo/demo1.png',
					tips:'点击查看示例'
				},
				/*
				,{
				    title: '柱状图自定义颜色',
					images:'column2.png',
					url:'demo/column',
					demo:null,
					tips:'更新中'
				}, {
				    title: '自定义图表背景颜色',
					images:'line.png',
					url:'demo/bgcolor',
					demo:null,
					tips:'更新中'
				},{
				    title: 'K线图与柱状图联动',
					images:'candle.png',
					url:'demo/candle',
					demo:null,
					tips:'更新中'
				},{
				    title: 'tab加swpier中引用多图表',
					images:'bar-contrast.png',
					url:'demo/swpier',
					demo:null,
					tips:'更新中'
				},{
				    title: '圆弧进度图自定义起始角度',
					images:'arc-bar.png',
					url:'demo/arcbar',
					demo:null,
					tips:'更新中'
				},{
				    title: '仪表盘自定义起始角度',
					images:'gauge.png',
					url:'demo/gauge',
					demo:null,
					tips:'更新中'
				}
				*/
			   ],
			};
		},
		components: {
			uniCard
		},
		methods: {
			clickCard(url) {
				uni.navigateTo({
					url: url
				});
			}
		}
	}
</script>

<style>
page{background-color: #f4f5f6;}
</style>
