// npm install -g cnpm --registry=https://registry.npm.taobao.org
// cnpm install express --save
// cnpm install body-parser --save
// cnpm install cookie-parser --save
// cnpm install multer --save

var express = require('express');
var app = express();
const bodyParser = require('body-parser');
const router = require('./router/index')  //  引入路由

app.use('/', express.static('public'));
 
app.use(bodyParser.urlencoded({
  extends: true
}));

//设置跨域访问
app.all('*', (req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
  res.header("X-Powered-By", ' 3.2.1');
  res.header("Content-Type", "application/json;charset=utf-8");
  next();
});


// app.get('/', function (req, res) {
   // res.send('Hello World');
   // // response = {
// //   message:'File uploaded successfully', 
// // };
// // res.end( JSON.stringify( response ) );
// })

//  使用路由 /api 是路由指向名称
app.use(`/api`,router)


// app.listen(8081);
var server = app.listen(80,'0.0.0.0', function () {
  var host = server.address().address
  var port = server.address().port 
  console.log("应用实例，访问地址为 http://%s:%s", host, port)
})

// node ex1.js