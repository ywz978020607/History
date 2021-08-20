var imageArr=[
  "/static/img/slide01.png",
  "/static/img/slide02.jpg",
  "/static/img/slide03.jpg",
  "/static/img/slide04.jpg",
];
//定义一个改变图片的方法
var count=1;
var timer;
function change(){
  var image=document.getElementById("slider_img");
  image.src=imageArr[count];

//  更新图片
  if(count==imageArr.length-1){
    count=0;
  }else{
    count++;
  }
}
//定义一个轮播的方法
function move(){
  timer=window.setInterval(change,2000);
}
//调轮播方法
window.onload=move();