//轮播图
var $li = $(".b_list ul li");
 var len = $li.length-1;
 var _index = 0;
 var $img = $(".b_main .b_m_pic li");
 var $btn = $(".b_btn div");

 var timer = null;
 $li.hover(function(){
     $(this).addClass("l_hover");
 },function(){
     $(this).removeClass("l_hover");
 });
 $li.click(function(){
     _index = $(this).index();
       $li.eq(_index).addClass("l_click").siblings().removeClass("l_click");
       $img.eq(_index).fadeIn().siblings().fadeOut();
     play();
 });
 function play(){
     $li.eq(_index).addClass("l_click").siblings().removeClass("l_click");
     $img.eq(_index).fadeIn().siblings().fadeOut();
 }
     $btn.click(function(){
         var index = $(this).index();
         if(index) {
             _index++;
             if (_index > len) {
                 _index = 0;
             }
             play();
         }else {
             _index--;
             if(_index < 0){
                 _index = len;
             }
             play();
         }
     });
 function auto(){
     timer = setInterval(function(){
         _index++;
         if(_index > len){
             _index = 0;
         }
         play();
     },4000);
 }
 //上面是计时器，调轮播速度可以改上面的2000那个值，单位毫秒2000ms=2s
 auto();
 $(".b_main").hover(function(){
     clearInterval(timer);
 },function(){
     auto();
 });
 $(".b_btn div").hover(function(){
     clearInterval(timer);
 },function(){
     auto();
 });
 
 /////////////////////////////////////////////////////////////////////
 
 /// 渲染 django
temp_page = 1; //当前页面
pages_all = 1; //所有页面

 $(function() {
    $( "#Button0" ).button();
    $( "#Button1" ).button();
     $( "#Button2" ).button();
     $( "#Button3" ).button();
     $( "#Button4" ).button();

     click1();//首页
});

//绑定监听 回车键
$('#input_page').bind('keypress', function (event) { 
    if (event.keyCode == "13") { 
        temp_page = $('#input_page').val();
        if(temp_page>0 && temp_page< pages_all){
            get_page();
        }
    }
})

function click0(){
    $('#show_news').empty();
    $('#show_news').append("waiting for search...");

    // get_search();
    setTimeout('get_search()',1000);
}

function click1(){
    temp_page = 1;
    get_page();
}
function click2(){
    temp_page -= 1;
    if(temp_page <=0){
        temp_page = 1;
    }
    get_page();
}
function click3(){
    temp_page += 1;
    if(temp_page > all_pages){
        temp_page = all_pages;   
    }
    get_page();
}
function click4(){
    temp_page = pages_all;
    get_page();
}

function get_page(){
    //使用全局变量 temp_page
    var params = {"mode":"0","page":temp_page,"ini_name":"index"};
    $.get('/api/', params, function(data){
        console.log(data);
        $('#show_news').empty();
        $('#show_news').append(data['data']);
        pages_all = parseInt(data['pages']);
        console.log(pages_all);
        $('#all_pages').empty();
        $('#all_pages').text(pages_all); //设置页数
        $('#temp_page').empty();
        $('#temp_page').text(`Page `+temp_page.toString()+` `);
        


        //设置不可点击
        if(temp_page===1){
            $("#Button2").hide();
        }
        else{
            $("#Button2").show();
        }
        if(temp_page===pages_all){
            $("#Button3").hide();
        }
        else{
            $("#Button3").show();
        }
    })
}


function get_search(){
    //使用全局变量 temp_page
    var params = {"mode":"1","context":document.getElementById('input1').value,"ini_name":"index"};
    $.get('/api/', params, function(data){
        console.log(data);
        $('#show_news').empty();
        $('#show_news').append(data['data']);

        $("#center1").hide();
    })
}


