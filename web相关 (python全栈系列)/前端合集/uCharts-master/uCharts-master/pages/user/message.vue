<template>
	<view class="qiun-center qiun-columns">
		<view>
			<image src="../../static/images/none.jpg" class="qiun-none"></image>
		</view>
		<view>
			<text class="qiun-text2">没有任何消息</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			
		}
	}
</script>

<style>
	page{background: #FFFFFF;}
.qiun-center{
	display: flex;
	display: -webkit-flex;
	align-items:center;
	justify-content:center;
	padding-top: 100upx;
}
.qiun-none{
	width: 391upx;
	height: 388upx;
}
.qiun-text2{
	font-size: 32upx;
	color: #666666;
}
</style>
