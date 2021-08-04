<template>
	<view style="padding-top: 40upx;">
		<view class="inputArea" style="text-align: center;">
			<image class="logo-img" src="../../static/images/avatar.png"></image>
		</view>
		<view class="inputArea">
			<input v-model="loginUsername" placeholder="请输入用户名" type="text" maxlength="11" class="inputClass" />
		</view>
		<view class="inputArea">
			<input v-model="loginPassword" placeholder="请输入登录密码" type="password" class="inputClass" />
		</view>
		<view style="padding: 0 10%;text-align: center;">
			<text style="color: red;">{{message}}</text>
		</view>
		<view class="inputArea">
			<button class="login-button" @click="goLogin">登 录</button>
		</view>
		<!--
		<view class="inputArea">
			<text style="float:right;color:blue;" @click="openRegisterPage">>>注册>></text>
		</view>
		-->
	</view>
</template>

<script>
	var _self;
	export default {
		data() {
			return {
				loginUsername: '',
				loginPassword: '',
				message: ''
			}
		},
		onLoad() {
			_self=this;
		},
		methods: {
			openRegisterPage() {
				uni.navigateTo({
					url: '../login/register',
					success: res => {},
					fail: () => {},
					complete: () => {}
				});
			},
			goLogin() {
				let loginUsername = this.loginUsername;
				let loginPassword = this.loginPassword;
				if (!loginUsername) {
					this.message = "用户名不能为空";
					return false;
				}
				if (!loginPassword) {
					this.message = "密码不能为空";
					return false;
				}
				uni.showLoading({
					title: '登录中...',
					mask: false
				});
				uni.request({
					url: 'https://www.easy-mock.com/mock/5cc586b64fc5576cba3d647b/uni-wx-charts/chartsdata2',
					method: 'get',
					data: {
						name: this.loginUsername,
						pw: this.loginPassword
					},
					success: res => {
						
						//这里都是假的，其实并没有在后台判断用户和密码
						if (_self.loginUsername=='ucharts' &&　_self.loginPassword=='123456') {
							let userinfo={
								avatarUrl:'../../static/images/avatar.png',
								name:'uCharts',
								phone:'13888888888',
								email:'admin@ucharts.cn'
							}
							uni.setStorageSync('userinfo', userinfo);
							uni.hideLoading();
							uni.reLaunch({
								url: 'index'
							});
						} else {
							uni.removeStorageSync('userinfo');
							this.message = '用户名或密码错误';
							uni.hideLoading();
						}
					},
					fail: () => {
						uni.hideLoading();
						this.message = "网络连接失败";
					},
					complete: () => {}
				});
			}
		}
	}
</script>

<style>
	.inputArea {
		padding: 30upx 10%;
	}

	.inputClass {
		border: 2px solid #ccc;
		border-radius: 44upx;
		outline: 0;
		width: 90%;
		padding: 16upx 30upx;
		background-color: #FFFFFF;
	}
	.logo-img {
		width: 150upx;
		height: 150upx;
		border-radius: 150upx;
	}
	.login-button {
		background: #2fc25b;
		color: #FFFFFF;
		border-radius: 44upx;
	}
</style>
