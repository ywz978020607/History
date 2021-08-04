<template>
	<view>
		<block v-for="(item, index) in info" :key="index">
			<view class="qiun-columns">
				<view class="qiun-rows qiun-list-title qiun-common-border-bottom" style="background-color: #f7f7fa;">
					<text style="flex: 1;">{{ item.title }}</text>
					<uni-icon color="#bbb" size="20" type="arrowup"></uni-icon>
				</view>
				<view class="qiun-bg-white qiun-list-sub" :class="item.open ? 'qiun-list-sub-active' : ''">
					<block v-for="(item2, index2) in item.sub" :key="index2">
						<view class="qiun-rows qiun-list-title qiun-common-border-bottom" @tap="openUrl('s='+index+'&id='+index2+'&t='+item2.title)" >
							<text style="flex: 1;">{{ item2.title }}</text>
							<uni-icon color="#bbb" size="20" type="arrowright"></uni-icon>
						</view>
					</block>
				</view>
			</view>
		</block>
	</view>
</template>

<script>
import uniIcon from '@/components/uni-ui/uni-icon/uni-icon.vue';

export default {
	components: {
		uniIcon
	},
	data() {
		return {
			info: [
				{
					title: '通用配置',
					sub: [
						{
							title: '基础配置'
						},
						{
							title: '数据配置'
						},
						{
							title: '标题配置'
						},
						{
							title: '坐标轴配置'
						}
					]
				},
				{
					title: '扩展配置',
					sub: [
						{
							title: '圆弧进度图'
						},
						{
							title: '仪表盘'
						},
						{
							title: '雷达图'
						},
						{
							title: '柱状图'
						},
						{
							title: '饼图圆环图'
						},
						{
							title: '折线图'
						},
						{
							title: '区域图'
						},
						{
							title: 'K线图'
						},
						{
							title: '条状图'
						},
						{
							title: '标记线'
						},
						{
							title: 'ToolTip'
						},
						{
							title: '其他配置'
						}
					]
				},
				{
					title: '方法&事件',
					sub: [
						{
							title: '更新图表数据'
						},
						{
							title: '停止动画效果'
						},
						{
							title: '添加监听事件'
						},
						{
							title: '获取点击序列编号'
						},
						{
							title: 'ToolTip方法'
						},
						{
							title: '图表拖拽事件'
						},
						{
							title: '放大或缩小X轴刻度'
						},
						{
							title: '图表渲染完成事件'
						}
					]
				}
			]
		};
	},
	methods: {
		openUrl(url) {
			uni.navigateTo({
				url: 'view?'+url
			});
		}
	}
};
</script>

<style>
page {
	display: flex;
	flex-direction: column;
	box-sizing: border-box;
	background-color: #f4f5f6;
}
.qiun-list-title {
	padding: 24upx 30upx;
	font-size: 32upx;
	flex: 1;
}
</style>
