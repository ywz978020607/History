function showModal() {  //打开上传框
	var modal = document.getElementById('modal');
	var overlay = document.getElementsByClassName('overlay')[0];
	overlay.style.display = 'block';
	modal.style.display = 'block';
}
function closeModal() {  //关闭上传框
	var modal = document.getElementById('modal');
	var overlay = document.getElementsByClassName('overlay')[0];
	overlay.style.display = 'none';
	modal.style.display = 'none';
}
//用DOM2级方法为右上角的叉号和黑色遮罩层添加事件：点击后关闭上传框
document.getElementsByClassName('overlay')[0].addEventListener('click', closeModal, false);
document.getElementById('close').addEventListener('click', closeModal, false);

//利用html5 FormData() API,创建一个接收文件的对象，因为可以多次拖拽，这里采用单例模式创建对象Dragfiles
var Dragfiles=(function (){
	var instance;
	return function(){
		if(!instance){
			instance = new FormData();
		}
		return instance;
	}
}());
//为Dragfiles添加一个清空所有文件的方法
FormData.prototype.deleteAll=function () {
	var _this=this;
	this.forEach(function(value,key){
		_this.delete(key);
	})
}

//添加拖拽事件
var dz = document.getElementById('content');
dz.ondragover = function (ev) {
	//阻止浏览器默认打开文件的操作
	ev.preventDefault();
	//拖入文件后边框颜色变红
	this.style.borderColor = 'red';
}

dz.ondragleave = function () {
	//恢复边框颜色
	this.style.borderColor = 'gray';
}
dz.ondrop = function (ev) {
	//恢复边框颜色
	this.style.borderColor = 'gray';
	//阻止浏览器默认打开文件的操作
	ev.preventDefault();
	var files = ev.dataTransfer.files;
	var len=files.length,
		i=0;
	var frag=document.createDocumentFragment();  //为了减少js修改dom树的频度，先创建一个fragment，然后在fragment里操作
	var tr,time,size;
	var newForm=Dragfiles(); //获取单例
	var it=newForm.entries(); //创建一个迭代器，测试用
	while(i<len){
		tr=document.createElement('tr');
		//获取文件大小
		size=Math.round(files[i].size * 100 / 1024) / 100 + 'KB';
		//获取格式化的修改时间
		time = files[i].lastModifiedDate.toLocaleDateString() + ' '+files[i].lastModifiedDate.toTimeString().split(' ')[0];
		tr.innerHTML='<td>'+files[i].name+'</td><td>'+time+'</td><td>'+size+'</td><td>删除</td>';
		console.log(size+' '+time);
		frag.appendChild(tr);
		//添加文件到newForm
		newForm.append(files[i].name,files[i]);
		//console.log(it.next());
		i++;
	}
	this.childNodes[1].childNodes[1].appendChild(frag);
	//为什么是‘1’？文档里几乎每一样东西都是一个节点，甚至连空格和换行符都会被解释成节点。而且都包含在childNodes属性所返回的数组中.不同于jade模板
}
function blink()
{
  document.getElementById('content').style.borderColor = 'gray';
}

//ajax上传文件
function upload(){
	if(document.getElementsByTagName('tbody')[0].hasChildNodes()==false){
		document.getElementById('content').style.borderColor = 'red';
		setTimeout(blink,200);
		return false;
	}
	var data=Dragfiles(); //获取formData
	$.ajax({
		url: 'http://39.105.218.125:80/upload/',
		type: 'POST',
		data: data,
		dataType:"json",
		async: true,
		cache: false,
		contentType: false,
		processData: false,
		success: function (msg) {
			alert(msg.status)  //可以替换为自己的方法
			//closeModal();
			//data.deleteAll(); //清空formData
			//$('.tbody').empty(); //清空列表
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
alert(XMLHttpRequest.status);
alert(XMLHttpRequest.readyState);
alert(textStatus);
} 
		
		
		
		//error: function (returndata) {
			//alert('finished!')  //可以替换为自己的方法
		//}
	});
}
// 用事件委托的方法为‘删除’添加点击事件，使用jquery中的on方法
$(".tbody").on('click','tr td:last-child',function(){
	//删除拖拽框已有的文件
	var temp=Dragfiles();
	var key=$(this).prev().prev().prev().text();
	console.log(key);
	temp.delete(key);
	$(this).parent().remove();
});
//清空所有内容
function clearAll(){
	if(document.getElementsByTagName('tbody')[0].hasChildNodes()==false){
		document.getElementById('content').style.borderColor = 'red';
		setTimeout(blink,300);
		return false;
	}
	var data=Dragfiles(); 
	data.deleteAll(); //清空formData
	//$('.tbody').empty(); 等同于以下方法
	document.getElementsByTagName('tbody')[0].innerHTML='';
}