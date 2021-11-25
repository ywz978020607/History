# jq-http

**读取**

```javascript
var param = {"limit_num":1,"id":"657447170","password":"dYzr8wSChJQIGCByNO3=8w85frU="};

function show(){
   	val = 0;
    $.ajaxSettings.async = false;  //修改为同步请求！！！
    $.get("/onenet_check/",param,function(data,status){
      // console.log(data);
      val = data;
      // $("#value0").text(data['datastreams'][1]['datapoints'][0]['value']);
      // $("#value1").text(data['datastreams'][0]['datapoints'][0]['value']);
     })
    return val;
}
```

- 注意: 如果需要定义为函数返回值，则在请求外部**定义变量**&设置为**同步**请求，然后赋值，在外部返回变量。

  

**写入**

```javascript
var param1 = {"limit_num":1,"id":"657447170","password":"dYzr8wSChJQIGCByNO3=8w85frU="};

function write(val){
    param1['data_name'] = JSON.stringify(['data2']) //可以多个
    param1['data_value'] = JSON.stringify([val]) //可以多个

    console.log(param1);
    $.get("/onenet_write/",param1,function(data,status){
      // console.log(data);
      alert("changed ok.");
      show();
     })
};
```

- 注意: 字典中夹带列表时，需要用`JSON.stringfy()` 序列化，然后再传，不然会错误解析为{'data_name[]':'data2'}

  

# axios

```javascript
<script src="https://cdn.staticfile.org/axios/0.18.0/axios.min.js"></script>

<script>
 //省略定义函数、调用函数
axios({
          method:'get',
          url:'/onenet_check/',
          params:{
              "limit_num":1,"id":"657447170","password":"dYzr8wSChJQIGCByNO3=8w85frU="
          }
          // responseType:'stream'
        }).then(response => {
            data = response.data
            console.log("axios::")
          console.log(data)
        }
      )
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
</script>

```



- 详细查看web备份/django备份/django-vue-plugin-bootstrap-jqhttp_axios文件夹进行测试 --test1v.html