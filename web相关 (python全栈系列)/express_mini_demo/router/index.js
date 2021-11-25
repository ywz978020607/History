const express = require("express")
const router = express.Router()


router.use((req, res, next) => {
  console.log("路由执行成功啦~~~", Date.now());
  next()  //一级一级地执行下来
})

//localhost/index/
router.get("/", (req, res, next) => {
  res.json({
    status: 200,
    data: "请求成功"
  })
})

//localhost/index/data/
router.get("/data", (req, res, next) => {
  var temp_json = {
    status: 200,
    data: [1, 2, 3, 4, 5, 6, 7]
  }
  res.json=temp_json;

})

module.exports = router