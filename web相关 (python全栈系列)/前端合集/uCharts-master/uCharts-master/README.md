## 喜讯！《uCharts高性能跨全端图表》荣获插件大赛一等奖，感谢DCloud以及mpvue团队的鼓励和认可！感谢各位开发者的问题反馈和赞赏！uCharts团队一定会不负众望，为大家打造完美、方便、高性能的图表而奋斗！再次感谢！
## 如遇到问题，请先参见页面最后章节【常见问题】解决，如没有您的问题，请在页面最下面【撰写评论】。几星不重要，重要的是解决您的问题。再次感谢您的支持与鼓励！！

## 最近更新
* [x] 2019.06.23 完善K线图，增加K线图与柱状图联动demo，详见`应用->K线图与柱状图联动`。
* [x] 2019.06.22 增加`opts.xAxis.labelCount`参数，X轴可见区域`标签数量`（即X轴数刻度标签单屏幕限制显示的数量），用于解决x轴文案问题。
* [x] 2019.06.22 优化拖拽事件，增加`opts.extra.touchMoveLimit` 图表拖拽时，每秒重新渲染的帧数`用于图表拖拽卡顿`。
* [x] 2019.06.17 增加updateData更新图表时，是否显示动画效果`animation` ，参见API更新图表方法。
* [x] 2019.06.17 增加updateData更新图表时，滚动条位置设置`scrollPosition`，参见API更新图表方法。


# [uCharts官方网站](https://www.ucharts.cn)
# <https://www.ucharts.cn>


# [在线文档](http://doc.ucharts.cn)


## QQ交流群:371774600
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/QQqrcode.png?raw=true)



## 快速体验

一套代码编到7个平台，依次扫描二维码，亲自体验uCharts图表跨平台效果！IOS因demo比较简单无法上架，请自行编译。

![](https://box.kancloud.cn/58092090f2bccc6871ca54dbec268811_654x479.png)


## [更新记录](https://www.kancloud.cn/qiun/ucharts/content/%E6%9B%B4%E6%96%B0%E8%AE%B0%E5%BD%95.md)

## 未来计划(V1.0至2.0版本)
- [ ] 2019.07.xx 计划加入雷达图等`ToolTip`事件
- [ ] 2019.07.xx 计划加入`组件内使用示例`
- [ ] 2019.07.xx 计划加入`条状图`、`分时图`、`玫瑰图`、`漏斗图`
- [ ] 2019.07.xx 推迟计划加入`第二种仪表盘样式`,增加[《亲手教您如何改造uCharts，打造您的专属图表》]()教程。
- [ ] 2019.07.xx 计划加入`渐变颜色填充`功能
- [ ] 2019.07.xx 计划修复折线图样式为曲线时，个别情况下曲线超出x轴的问题。
- [ ] 2019.06.xx 计划加入`辅助线（标记线）`功能，支持`柱状图、折线图、区域图、K线图`


## 未来计划(全新V2.0版本)
## 2019.5.20重要又浪漫的日期，uCharts团队正式建立了，我们将以追求极致、追求完美的极客精神来打造uCharts。uCharts2.0版本正在前期策划中，将以全新结构重写uCharts，支持多Y轴、多X轴、自定义图例位置、以及更多图表类型，请各位敬请期待。

## 支持图表类型
- 饼图   `pie`
- 圆环图 `ring`
- 线图   `line`（直线、曲线）
- 柱状图 `column`（分组、堆叠、温度计）
- 区域图 `area`（直线、曲线）
- 雷达图 `radar`
- 圆弧进度图 `arcbar`
- 仪表盘 `gauge`
- K线图  `candle`(完善中)
- 条状图 `bar`(开发中)
- 混合图 `mix`（支持point、line直线曲线、column、area直线曲线）


## 插件特点
- 改造后的插件可以跨端使用，支持H5、小程序（微信/支付宝/百度/头条）、APP，调用简单方便、性能及体验极佳。
- 虽然没有Echarts及F2图表功能强大，但可以实现一套业务逻辑各端通用，并解决了支付宝小程序图表显示模糊等问题。
- 支持单页面多图表，demo中单页10个图表，响应速度超快。
- 支持入场动画及ToolTip动画效果。
- 独特支持`横屏模式`感谢`masterLi`提供需求。

## 为何不用Echarts？
- 相比Echarts及F2的复杂的设置，本插件几乎等于傻瓜式的配置。
- Echarts在跨端使用更复杂，本插件只需要简单的两个`<canvas>`标签轻松区别搞定，代码整洁易维护。
- Echarts在IOS端图表显示错位，只能引用网页解决。
- 本插件打包后的体积相比Echarts小很多很多，所以性能更好。
- 如果您是uni-app初学者，那么强烈建议您使用uCharts，并且目前可以跨全端通用，减少工作量，增强一致性体验。
- 图表样式均可自定义，懂js的都可以读懂插件源码，直接修改u-charts.js源码即可。
- 本插件经过大量测试，反复论证并加以改造而成，请各位放心使用。

## uni-app图表选型参考流程

![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/xuanxing.png?raw=true)

## 亲手教您如何改造uCharts，打造您的专属图表
- 为何要改造uCharts?
- 并不是所有图表插件直接拿来就可以满足客户需求，如果您的UI设计师设计一个图表，如下图:

![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/example.gif?raw=true)

- 您会发现这个图表即使在echarts里也不是很好实现，那么就需要我们自己动手去实现。下面就让我们一起来完成，本文旨在抛砖引玉，希望各位朋友能够更好的应用uCharts来完成您的项目，如果您有更好的设计，请提交您的PR到github[uCharts跨端图表](https://github.com/16cheng/uCharts)，帮助更多朋友，感谢您的付出及贡献！

## [uCharts跨端图表改造教程（暂未完成，请关注）]()


## 图表示例
![](https://box.kancloud.cn/1d5e2c60898de86f5f33f93020ff029e_468x342.gif)
![](https://box.kancloud.cn/63e5833a7ccd8308b0f8ab59522c36c1_468x349.gif)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/mix.gif?raw=true)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/mix2.gif?raw=true)
![](https://box.kancloud.cn/2f00fcf5a8ce7a9593aea3bc14b8f150_468x411.gif)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/yibiaopan.gif?raw=true)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/arcbar.gif?raw=true)
![](https://box.kancloud.cn/af4fb86f40538d85da3e8def8669b87d_468x342.gif)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/lineA.gif?raw=true)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/lineA-scroll.gif?raw=true)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/dashLine.gif?raw=true)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/area.gif?raw=true)
![](https://box.kancloud.cn/1a7b5b2908751cbb3f135e5071e42f1b_468x345.gif)
![](https://box.kancloud.cn/a3c42919a45fbf93db028fe9a0975adc_468x345.gif)
![](https://box.kancloud.cn/fe5f988bfb017c5d46d695e4626bd656_468x345.gif)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/radar.gif?raw=true)
![](https://github.com/16cheng/uCharts/blob/master/example/uni-app/static/lineB.gif?raw=true)


## 常见问题

各位遇到问题请先参考以下问题，如果仍不能解决，请留言。

### 通用问题
- 如果用在您的项目上图表不显示，请先运行demo页面，如果demo页面也无法显示，请查看全局样式是否定义了`canvas的样式`，如有请取消。
- 如发现实例化图表后，`客户端卡死`的状况，请在实例化图表前（即调用`showColumn(canvasId,chartData)`前）检查传入图表数组（`chartData.categories`和`chartData.series`）是否为空，如果为空则不要实例化图表。后续将在源码中解决此问题。
- 图表`背景颜色`问题，很多朋友设置图表背景颜色时候，只修改了view和canvas的css,忘记了修改实例化参数中的`background:'#FFFFFF'`，导致图表画板右侧有一道白条（这个是图表配置中的右边距），所以特修改了demo中的`柱状图`的背景颜色供大家参考。

### 支付宝、百度、头条问题
- 在高分屏模式下，如果发现图表已显示，但位置不正确，请检查上级`view`容器的`样式`，为了解决高分屏canvas模糊问题，使用了css的`transform`，所以请修改上级样式使canvas容器缩放至相应位置。
- 如果将canvas放在多级<view>组件下，遇到ToolTip不显示或点击区域不正确，请在`touch`事件中增加以下代码解决。
```javascript
//#ifdef MP-ALIPAY || MP-BAIDU || MP-TOUTIAO
e.mp.currentTarget.offsetTop+=uni.upx2px(510);
//#endif
```
> `uni.upx2px(510);`是canvas组件的上级<view>组件的高度

### 组件问题
- 很多小伙伴们自行把本插件做成组件来调用，做成组件需要注意，如果涉及到v-if切换显示图表组件，第二次可能会变空白，这里有两个建议：
1、建议用v-show替代v-if切换显示图表组件。
2、建议参考demo，不要将canvas做到组件里使用，即直接写在主页面中。
### 初步解决`组件内使用问题`，感谢`342805357@qq.com`提出组件问题解决方案，增加`opts.$this`参数，组件使用时实例化前请传递this。后续会增加组件使用示例，请关注。

# `支付宝小程序IDE中不显示，但运行到真机是可以显示的，请真机测试。`