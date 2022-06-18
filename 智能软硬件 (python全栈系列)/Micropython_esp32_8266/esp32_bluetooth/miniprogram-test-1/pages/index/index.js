//index.js
//获取应用实例
const app = getApp()
var temp1 = '';
var temp2 = '';

Page({
  data: {
    motto1: '回复的消息',
    motto2: '',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }

    setInterval(function () {
      this.test();

      this.setData({
        motto1: temp1,
        motto2: temp2,
      })
    }.bind(this), 1000);

  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },


  test: function () {
    wx.request({
      url: 'https://api.heclouds.com/devices/532451082/datapoints',
      header: {
        "api-key": 'rxwlcmCkRWye4nGnQ=OUeEJ4Wy0='
      },
      data: {
        "limit": (1)
      },
      method: "GET",
      success: function (res) {
        console.log(res.data.data);
        temp2 = res.data.data.datastreams["0"].datapoints[0].at;
        temp1 = res.data.data.datastreams["1"].datapoints[0].value;
      },
    })
  },


  down1Input: function (e) {
    this.setData({
      down1: e.detail.value
    })
  },


  Btn1: function (e) {
    wx.request({
      url: 'https://api.heclouds.com/devices/532451082/datapoints',
      header: {
        "api-key": 'rxwlcmCkRWye4nGnQ=OUeEJ4Wy0=',
      },
      data: {
        "datastreams": [{ "id": "outside", "datapoints": [{ "value": this.data.down1 }] }],
      },
      method: "POST",
      success: function (res) {
        console.warn("success back!");
        console.log(res);
        wx.showToast({
          title: '设置成功',
          duration: 2000
        })
      },
    });
    this.setData({
      down1: ''
    })
  },




})
