
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
    var params = {"mode":"0","page":temp_page,"ini_name":"publish"};
    $.get('http://127.0.0.1:8000/api/', params, function(data){
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
    var params = {"mode":"1","context":document.getElementById('input1').value,"ini_name":"publish"};
    $.get('http://127.0.0.1:8000/api/', params, function(data){
        console.log(data);
        $('#show_news').empty();
        $('#show_news').append(data['data']);

        $("#center1").hide();
    })
}


