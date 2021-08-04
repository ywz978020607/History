export default [
[//0
	[//0.0
	"opts | Object |  |  ",
	"opts.$this | Object | required | this实例组件内使用图表，必须传入this实例 ",
	"opts.canvasId | String | required | 页面组件canvas-id，支付宝中为id ",
	"opts.width | Number | required | canvas宽度，单位为px，支付宝高分屏需要乘像素比 ",
	"opts.height | Number | required | canvas高度，单位为px，支付宝高分屏需要乘像素比 ",
	"opts.type | String | required | 图表类型，可选值为pie、 line、 column、 area、 ring、 radar、 arcbar、 gauge、 candle、 bar、 mix ",
	"opts.pixelRatio | Number | required | 像素比，默认为1，非H5端引用无需设置 ",
	"opts.rotate | Boolean | 默认false | 横屏模式，默认为false ",
	"opts.rotateLock | Boolean | 默认false | 锁定横屏模式，如果在支付宝和百度小程序中使用横屏模式，请赋值true，否则每次都会旋转90度。跨端使用通过uni-app的条件编译来赋值 ",
	"opts.fontSize | Number | 默认13px | 全局默认字体大小（可选，单位为px，默认13px）高分屏不必乘像素比，自动根据pixelRatio计算 ",
	"opts.background | String |  | canvas背景颜色（如果页面背景颜色不是白色请设置为页面的背景颜色，默认#ffffff） ",
	"opts.enableScroll | Boolean | 默认false | 是否开启图表可拖拽滚动 默认false 支持line、area、 column、 candle图表类型(需配合绑定@touchstart、 @touchmove、  @touchend方法) ",
	"opts.enableMarkLine | Boolean | 默认false | 是否显示辅助线 默认false 支持line、 area、 column、 candle图表类型 ",
	"opts.animation | Boolean | 默认为 true | 是否动画展示 ",
	"opts.legend | Boolen | 默认为 true | 图例设置，是否显示图表下方各类别的标识 ",
	"opts.dataLabel | Boolean | 默认为 true | 是否在图表中显示数据标签内容值 ",
	"opts.dataPointShape | Boolean | 默认为 true | 是否在图表中显示数据点图形标识 ",
	"opts.disablePieStroke | Boolean | 默认为 false | 不绘制饼图（圆环图）各区块的白色分割线`即将迁移至扩展配置中` "
	],[//0.1
	"opts.categories | Array | required | 数据类别(饼图、圆环图不需要) ",
	"opts.categories.value | Number |  | 仅仪表盘有效，定义仪表盘分段值 ",
	"opts.categories.color | String |  | 仅仪表盘有效，定义仪表盘分段背景颜色 ",
	"opts.series | Array | required | 数据列表 ",
	"opts.series.data | Array | required | (饼图、圆环图为Number) 数据，如果传入null图表该处出现断点 ",
	"opts.series.data.value | Number |  | 仅针对柱状图有效，主要作用为柱状图自定义颜色 ",
	"opts.series.data.color | String |  | 仅针对柱状图有效，主要作用为柱状图自定义颜色 ",
	"opts.series.color | String |  | 例如#7cb5ec 不传入则使用系统默认配色方案 ",
	"opts.series.name | String |  | 数据名称 ",
	"opts.series.type | String |  | `混合图表`图形展示方式，有效值为point、line、column详细使用方法见demo ",
	"opts.series.disableLegend  | String | 默认false | `混合图表`中禁止显示ToolTip图例，默认false即默认显示该类别图例",
	"opts.series.style | String | 默认straight | 暂时定义为`混合图表折线图样式`，有效值为`curve`曲线,`straight`直线 ",
	"opts.series.shape | String | 默认为 circle | 图例样式，有效值为diamond:◇， circle:○， triangle:△， rect:□ ",
	"opts.series.format | Function |  | 自定义显示数据内容 "
	],[//0.2
	"opts.title | Object |  | 适用于`ring`、`arcbar`、`gauge` ",
	"opts.title.name| String |  | 标题内容 ",
	"opts.title.fontSize | Number |  | 标题字体大小（可选，单位为px） ",
	"opts.title.color | String |  | 标题颜色（可选） ",
	"opts.title.offsetX | Number | 默认0px | 标题横向位置偏移量，单位px，默认0 ",
	"opts.title.offsetY | Number | 默认0px | 标题纵向位置偏移量，单位px，默认0 ",
	"opts.subtitle | Object |  | 适用于`ring`、`arcbar`、`gauge` ",
	"opts.subtitle.name | String |  | 副标题内容 ",
	"opts.subtitle.offsetX | Number | 默认0px | 副标题横向位置偏移量，单位px，默认0 ",
	"opts.subtitle.offsetY | Number | 默认0px | 副标题横向位置偏移量，单位px，默认0 ",
	"opts.subtitle.fontSize | Number |  | 副标题字体大小（可选，单位为px） ",
	"opts.subtitle.color | String |  | 副标题颜色（可选） "
	],[//0.3
	"opts.xAxis | Object |  | X轴配置 ",
	"opts.xAxis.rotateLabel | Boolean | 默认为 false | X轴刻度（数值）标签是否旋转（仅在文案超过单屏宽度时有效） ",
	"opts.xAxis.itemCount | Number | 默认为 5 | X轴可见区域`数据数量`（即X轴数据密度），配合拖拽滚动使用（即仅在启用enableScroll时有效） ",
	"opts.xAxis.labelCount | Number | | X轴可见区域`标签数量`（即X轴数刻度标签单屏幕限制显示的数量）",
	"opts.xAxis.scrollShow | Boolean | 默认为 false | 是否显示滚动条，配合拖拽滚动使用（即仅在启用enableScroll时有效） ",
	"opts.xAxis.scrollAlign | String | 默认为 left | 滚动条初始位置，left为数据整体左对齐，right为右对齐 ",
	"opts.xAxis.scrollBackgroundColor | String | 默认为 #EFEBEF | X轴滚动条背景颜色，配合拖拽滚动使用（即仅在启用enableScroll时有效） ",
	"opts.xAxis.scrollColor | String | 默认为 #A6A6A6 | X轴滚动条颜色，配合拖拽滚动使用（即仅在启用enableScroll时有效） ",
	"opts.xAxis.disabled | Boolean | 默认为 false | 不绘制X轴 ",
	"opts.xAxis.disableGrid | Boolean | 默认为 false | 不绘制X轴网格(即默认绘制网格) ",
	"opts.xAxis.type | String | 默认为calibration | X轴网格样式，可选值calibration（刻度）、grid（网格） ",
	"opts.xAxis.gridColor | String | 默认为 #cccccc | X轴网格颜色 例如#7cb5ec ",
	"opts.xAxis.gridType | String | 默认为 solid | X轴网格线型 'solid'为实线、'dash'为虚线\` ",
	"opts.xAxis.dashLength | Number | 默认为 4px | X轴网格为虚线时，单段虚线长度 ",
	"opts.xAxis.fontColor | String | 默认为 #666666 | X轴数据点颜色 例如#7cb5ec ",
	"opts.yAxis | Object |  | Y轴配置 ",
	"opts.yAxis.format | Function |  | 自定义Y轴文案显示 ",
	"opts.yAxis.min | Number |  | Y轴起始值 ",
	"opts.yAxis.max | Number |  | Y轴终止值 ",
	"opts.yAxis.title | String |  | Y轴title ",
	"opts.yAxis.disabled | Boolean | 默认为 false | 不绘制Y轴 ",
	"opts.yAxis.disableGrid | Boolean | 默认为 false | 不绘制Y轴网格(即默认绘制网格) ",
	"opts.yAxis.splitNumber | Number | 默认5 | Y轴网格数量 ",
	"opts.yAxis.gridType | String | 默认为 solid | Y轴网格线型 'solid'为实线、'dash'为虚线 ",
	"opts.yAxis.dashLength | Number | 默认为 4px | Y轴网格为虚线时，单段虚线长度 ",
	"opts.yAxis.gridColor | String | 默认为 #cccccc | Y轴网格颜色 例如#7cb5ec ",
	"opts.yAxis.fontColor | String | 默认为 #666666 | Y轴数据点颜色 例如#7cb5ec ",
	"opts.yAxis.titleFontColor | String | 默认为 #333333 | Y轴title颜色 例如#7cb5ec "
	]
],[//1
	[//1.0
	"opts.extra.arcbar| Object |   |圆弧进度图相关配置",
	"opts.extra.arcbar.type| String | 默认default |圆弧进度图样式，default为半圆弧，circle为整圆",
	"opts.extra.arcbar.width| Number | 默认12px |圆弧进度图弧线宽度，单位为px",
	"opts.extra.arcbar.backgroundColor| String | 默认#E9E9E9 |圆弧进度图背景颜色",
	"opts.extra.arcbar.startAngle| Number | 默认0.75 |圆弧进度图起始角度，0-2之间，0为3点钟位置，0.5为6点钟，1为9点钟，1.5为12点钟",
	"opts.extra.arcbar.endAngle| Number | 默认0.25 |圆弧进度图结束角度，0-2之间，0为3点钟位置，0.5为6点钟，1为9点钟，1.5为12点钟"
	],[//1.1
	"opts.extra.gauge| Object | |仪表盘相关配置",
	"opts.extra.gauge.type| String | 默认default |仪表盘样式，default为百度样式，`其他样式开发中`",
	"opts.extra.gauge.width| Number | 默认15px |仪表盘坐标轴（指示盘）线宽度，单位为px",
	"opts.extra.gauge.labelColor| String | 默认#666666|仪表盘刻度尺标签文字颜色",
	"opts.extra.gauge.startAngle| Number | 默认0.75 |仪表盘起始角度，0-2之间，0为3点钟位置，0.5为6点钟，1为9点钟，1.5为12点钟",
	"opts.extra.gauge.endAngle| Number | 默认0.25 |仪表盘结束角度，0-2之间，0为3点钟位置，0.5为6点钟，1为9点钟，1.5为12点钟",
	"opts.extra.gauge.startNumber| Number | 默认0 |仪表盘起始数值",
	"opts.extra.gauge.endNumber| Number | 默认100 |仪表盘结束数值",
	"opts.extra.gauge.splitLine| Object | |仪表盘刻度线配置",
	"opts.extra.gauge.splitLine.fixRadius| Number | 默认0 |仪表盘刻度线径向偏移量",
	"opts.extra.gauge.splitLine.splitNumber| Number | 默认10 |仪表盘刻度线分段总数量",
	"opts.extra.gauge.splitLine.width| Number | 默认15px |仪表盘分割线长度",
	"opts.extra.gauge.splitLine.color| String | 默认#FFFFFF |仪表盘分割线颜色",
	"opts.extra.gauge.splitLine.childNumber| Number | 默认5 |仪表盘子刻度线数量",
	"opts.extra.gauge.splitLine.childWidth| Number | 默认5px |仪表盘子刻度线长度",
	"opts.extra.gauge.pointer| Object | |仪表盘指针配置",
	"opts.extra.gauge.pointer.width| Number | 默认15px |仪表盘指针宽度",
	"opts.extra.gauge.pointer.color| String | 默认auto |仪表盘指针颜色，定义为auto时，随仪表盘背景颜色改变,或者可以指定颜色例如#7cb5ec"
	],[//1.2
	"opts.extra.radar| Object | |雷达图相关配置",
	"opts.extra.radar.max| Number|默认为 series |data的最大值，数据区间最大值，用于调整数据显示的比例",
	"opts.extra.radar.labelColor |String|默认为 #666666|各项标识文案的颜色",
	"opts.extra.radar.gridColor |String| 默认为 #cccccc| 雷达图网格颜色"
	],[//1.3
	"opts.extra.column| Object | |柱状图相关配置",
	"opts.extra.column.type| Object | 默认group |柱状图类型：group分组柱状图，stack为堆叠柱状图（未完成开发中），meter为温度计式图",
	"opts.extra.column.width |Number| | 柱状图每项的图形宽度，单位为px",
	"opts.extra.column.meter |Object | | 温度计式图配置项",
	"opts.extra.column.meter.border |Number| | 边框宽度，单位为px，默认1px",
	"opts.extra.column.meter.fillColor| String | 默认#FFFFFF |空余填充颜色"
	],[//1.4
	"opts.extra.pie| Object| | 饼图、圆环图相关配置",
	"opts.extra.pie.activeOpacity | Number | required |启用Tooltip点击时，突出部分的透明度，默认0.5 ",
	"opts.extra.pie.offsetAngle| Number| 默认为0| 起始角度偏移度数，顺时针方向，起点为3点钟位置（比如要设置起点为12点钟位置，即逆时针偏移90度，传入-90即可）",
	"opts.extra.pie.lableWidth| Number | required  |数据标签到饼图外圆连线的长度，必填参数，否则报错，单位为px",
	"opts.extra.pie.ringWidth| Number | |ringChart圆环宽度，单位为px"
	],[//1.5
	"opts.extra.line| Object | | 折线图配置 ",
	"opts.extra.line.type | String| 默认straight | 可选值：curve曲线，straight直线 ",
	"opts.extra.line.width| Number| 默认2px | 折线宽度 "
	],[//1.6
	"opts.extra.area| Object | | 区域图配置 ",
	"opts.extra.area.type | String| 默认straight | 可选值：curve曲线，straight直线 ",
	"opts.extra.area.opacity| Number| 默认0.2 | 区域图透明度 ",
	"opts.extra.area.addLine | Boolean | 默认false | 是否叠加相应的折线 ",
	"opts.extra.area.width| Number| 默认2px | 折线宽度 "
	],[//1.7
	"opts.extra.candle| Object | |K线图相关配置",
	"opts.extra.candle.color| Object | |K线图颜色配置",
	"opts.extra.candle.color.upLine| String | 默认#f04864 |K线图为涨时线颜色",
	"opts.extra.candle.color.upFill| String | 默认#f04864 |K线图为涨时填充颜色",
	"opts.extra.candle.color.downLine| String | 默认#2fc25b |K线图为跌时线颜色",
	"opts.extra.candle.color.downFill| String | 默认#2fc25b |K线图为跌时填充颜色",
	"opts.extra.candle.average| Object | |均线设置",
	"opts.extra.candle.average.show | Boolean | 默认false |是否显示均线",
	"opts.extra.candle.average.name | `Array` |  |均线名称（例如['MA5','MA20']）用于下方图例显示",
	"opts.extra.candle.average.day | `Array` |  |均线单位日期（例如[5,20]为显示5日及20日均线）",
	"opts.extra.candle.average.color | `Array` |  |均线颜色，例如['#1890ff', '#2fc25b']"
	],[//1.8
	"opts.extra.bar| Object | |条状图相关配置`开发中`",
	"opts.extra.bar.type| Object | 默认group |条状图类型：`group`分组条状图，`stack`为堆叠条状图`开发中`",
	"opts.extra.bar.width |Number| | 条状图每项的图形宽度，单位为px`开发中`"
	],[//1.9
	"opts.extra.markLine |Object | | 在柱状图、折线图、区域图、K线图中额外增加水平直线，仅在`opts.enableMarkLine`为true时显示",
	"opts.extra.markLine.type |String | 默认为 solid| 线型 'solid'为实线、'dash'为虚线",
	"opts.extra.markLine.dashLength |Number | 默认为 4px | 单段虚线长度  ",
	"opts.extra.markLine.data |`Array` | | 辅助线数据，请传入`数组`类型，支持多条辅助线",
	"opts.extra.markLine.data.value |Number | | 辅助线数值",
	"opts.extra.markLine.data.color |String | 默认为 #| 辅助线颜色",
	"opts.extra.markLine.data.label |Boolean| 默认为 false | 是否显示数据标签",
	"opts.extra.markLine.data.labelBgColor |String | 默认为# | 数据标签背景颜色 ",
	"opts.extra.markLine.data.labelBgOpacity |String | 默认为# | 数据标签背景颜色透明度 ",
	"opts.extra.markLine.data.labelAlign |String | 默认为left | 数据标签显示位置，有效值left和right "
	],[//1.10
	"opts.extra.tooltip |Object | | ToolTip设置",
	"opts.extra.tooltip.bgColor| String | 默认#000000 | ToolTip背景颜色",
	"opts.extra.tooltip.bgOpacity | Number | 默认0.7 | ToolTip背景颜色透明度",
	"opts.extra.tooltip.gridType | String | 默认为 solid | 分割线线型 'solid'为实线、'dash'为虚线 ",
	"opts.extra.tooltip.dashLength | Number | 默认为 4px | 分割线为虚线时，单段虚线长度 ",
	"opts.extra.tooltip.gridColor | String | 默认为 # | 分割线颜色 ",
	"opts.extra.tooltip.fontColor | String | 默认为 #FFFFFF| 文字颜色 例如#7cb5ec ",
	"opts.extra.tooltip.horizentalLine| Boolean| 默认为 false| 是否显示水平横线 ",
	"opts.extra.tooltip.xAxisLabel |Boolean| 默认为 false | 是否显示数据标签",
	"opts.extra.tooltip.yAxisLabel |Boolean| 默认为 false | 是否显示数据标签",
	"opts.extra.tooltip.labelBgColor |String | 默认为#000000 | 数据标签背景颜色 ",
	"opts.extra.tooltip.labelBgOpacity |Number | 默认为0.7 | 数据标签背景颜色透明度 ",
	"opts.extra.tooltip.labelFontColor  |String | 默认为# | 数据标签文字颜色 ",
	"opts.extra.tooltip.activeBgColor |String |默认为#000000 | 仅柱状图类适用，当前点击柱状图的背景颜色 ",
	"opts.extra.tooltip.activeBgOpacity |Number |默认0.08 | 仅柱状图类适用，当前点击柱状图的背景颜色透明度 "
	],[//1.11
	"opts.extra.legendTextColor |String | 默认为 #cccccc | 图例文案颜色 例如#7cb5ec`后期将变更为opts.legend.textColor迁移到基础配置里`",
	"opts.extra.touchMoveLimit |Number | 默认为20 | 图表拖拽时，每秒重新渲染的帧数`用于图表拖拽卡顿`"
	]
],[//2
	[//2.0
		" updateData(data) | Function |  | 例如LineA.updateData({data}) ",
		"data | Object|  | 更新的数据 ",
		"data.categories| Array | 当前实例categories  | 同opts.categories ",
		"data.series| Array | 当前实例series | 同opts.series",
		"data.title| Array | 当前实例title | 同opts.title",
		"data.subtitle| Array | 当前实例subtitle | 同opts.subtitle",
		"data.scrollPosition| String | current | 开启图表拖拽后，更新图表后图表时，滚动条的偏移距离，可选值`left`更新后强制左对齐；`right`更新后强制右对齐；`current`更新后保持当前偏移距离",
		" data.animation | Boolean | 当前实例animation  | 是否动画展示 "
	],[//2.1
		"stopAnimation()  |  |  | 停止当前正在进行的动画效果，直接展示渲染的最终结果"
	],[//2.2
		"addEventListener(type, listener)  |  |  | 添加事件监听，type: String事件类型，listener: function 处理方法"
	],[//2.3
		"getCurrentDataIndex(e) |  |  | 获取图表中点击时的数据序列编号(-1表示未找到对应的数据区域), e: Object微信小程序标准事件，需要手动的去绑定touch事件，具体可参考wx-charts-demo中column图示例"
	],[//2.4
		"showToolTip(e, options?) |  |  | 图表中展示数据详细内容(目前仅支持line和area图表类型)，e: Object微信小程序标准事件，options: Object可选，tooltip的自定义配置，支持option.background，默认为#000000; option.format, function类型，接受两个传入的参数，seriesItem(Object, 包括seriesItem.name以及seriesItem.data)和category，可自定义tooltip显示内容。具体可参考ucharts-demo中line图示例"
	],[//2.5
		"scrollStart(e), scroll(e),scrollEnd(e) |  |  | 设置支持图表拖拽系列事件(支持line, area, column)，具体参考wx-charts-demo中ScrollLine图示例"
	],[//2.6
		"zoom(val) |  |  | 启用滚动条时，放大或缩小屏幕范围内数据数量。"
	],[//2.7
		"renderComplete |  |  | 图表渲染完成（如果有动画效果，则动画效果完成时触发）"
	]
]
]
