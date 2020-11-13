const express = require("express")
const router = express.Router()
const config = require("./config"); //require 可以./

router.use((req, res, next) => {
  console.log("路由执行成功啦~~~", Date.now());
  next()  //一级一级地执行下来
})

//localhost/api/
router.get("/", (req, res, next) => {
  console.log(req.query);
  every_page_num = 10; //每页条目
  mode = req.query.mode;
  var ret = {}

  if(mode=='0'){
    //查询
    page = req.query.page;
    ini_name = req.query.ini_name;

    var c =new config("router/"+ini_name+".ini") //否则从ex1.js目录开始
    var ret_c = c.readAll()
    var keys_list = Object.keys(ret_c)
    var all_len = keys_list.length;

    if(all_len%every_page_num!=0){
      ret['pages']=parseInt(all_len/every_page_num)+1
    }
    else{
      ret['pages']=parseInt(all_len/every_page_num)
    }
    ret['data']=''
    //从后向前找
    start_ii = all_len - page*every_page_num
    if(start_ii<0){start_ii=0}
    for(var ii=start_ii+every_page_num-1;ii>start_ii-1;ii--){
      ret['data'] += ret_c[ii.toString()];
    }
    res.json(ret)
    return
  }
  else if(mode=='1'){
    //.toLowerCase()
    context = req.query.context.toLowerCase();
    var c =new config("router/"+ini_name+".ini") //否则从ex1.js目录开始
    var ret_c = c.readAll()
    var keys_list = Object.keys(ret_c)
    var all_len = keys_list.length;
    ret['data']='';
    for(var ii=0;ii<all_len;ii++){
      if((ret_c[ii.toString()].toLowerCase().search(context)) != -1){
        ret['data'] += ret_c[ii.toString()]
      }
    }
    res.json(ret)
    return
  }

  res.json({
    status: 200,
    data: "res nothing"
  })

  
})

//localhost/api/data/
router.get("/data", (req, res, next) => {
  var temp_json = {
    status: 200,
    data: [1, 2, 3, 4, 5, 6, 7]
  }
  res.json=temp_json;

})

module.exports = router