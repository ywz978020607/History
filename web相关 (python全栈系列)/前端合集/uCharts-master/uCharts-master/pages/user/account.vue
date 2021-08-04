<template>
	<view style="padding-top: 40upx;">
		<view style="padding: 0 10%;">
			<view class="listcell">
					用户名:{{userinfo.name}}
			</view>
			<view class="listcell">
					电话:{{userinfo.phone}}
			</view>
			<view class="listcell">
					邮箱:{{userinfo.email}}
			</view>
			<view style="margin-top: 80upx;">
					<button class="login-button" @click="logout">退 出</button>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				userinfo: '',
			}
		},
		onLoad() {
			console.log('logout页面onLoad');
			this.userinfo = uni.getStorageSync('userinfo');
		},
		methods: {
			logout() {
				uni.showLoading({
					title: 'waiting',
					mask: false
				});
				
				uni.removeStorageSync('userinfo');
						
				uni.hideLoading();
				uni.reLaunch({
					url: 'index'
				});
				
				
				
			}
		}
	}
</script>

<style>
.listcell{
	padding: 20upx 0;
	border-bottom: 1px solid #ccc;
}
.login-button {
		background: #E3162E;
		color: #FFFFFF;
		border-radius: 44upx;
	}
</style>
