<!--
function $mm(obj){
   return (typeof obj == "object")?obj:document.getElementById(obj);;
}
//js操作cookie
function SetCookie(name,value){
	var minute = 10000; //保存天数
	var exp = new Date();
	exp.setTime(exp.getTime() + minute*60*1000*60*24);
	document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}
function getCookie(name){//取cookies函数
	var arr = document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)"));
	if(arr != null) return unescape(arr[2]); return null;
}
function delCookie(name)//删除cookie
{
	var exp = new Date();
	exp.setTime(exp.getTime() - 1);
	var cval=getCookie(name);
	if(cval!=null) document.cookie= name + "="+cval+";expires="+exp.toGMTString();
}
//插入回复@
function backcomment(msg){
	$mm('content').value=$mm('content').value+"@"+msg;
}
//页面元素添加行
var row_count = 0;
function addNew()
{
var table1 = $('#table1');
var firstTr = table1.find('tbody>tr:first');
var row = $("<tr></tr>");
var td = $("<td></td>");
var td1 = $("<td></td>");
var td2 = $("<td></td>");
var td3 = $("<td></td>");
td.append($("<select name='eletype"+row_count+"' id='eletype"+row_count+"'><option value ='文本框'>文本框</option> <option value ='按钮'>按钮</option> <option value ='单选框'>单选框</option> <option value ='复选框'>复选框</option> </select>"));
td1.append($("<input type='text' style='width: 300px;' name='elexpath"+row_count+"' id='elexpath"+row_count+"' value=''>"));
td2.append($("<input type='text' name='elevalue"+row_count+"' id='elevalue"+row_count+"' value=''>"));
td3.append($("<a href='javascript:void(0)' onclick='return del(this)'>删除</a>"));
row.append(td);
row.append(td1);
row.append(td2);
row.append(td3);
table1.append(row);
row_count++;
}

//删除页面元素
function del(ele) {
	$(ele).parent().parent().remove();
}

function $mmajax(){
	var url=arguments[0]||""; 
	var queryStr=arguments[1]||""; 
	if(window.ActiveXObject){  
		xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");  
	}else if(window.XMLHttpRequest){
		xmlHttp = new XMLHttpRequest();  
	}
	if(0==xmlHttp.readyState || 4==xmlHttp.readyState){
		var browserflag=true;
		if(isFirefox=navigator.userAgent.indexOf("Firefox")>0){
			browserflag=false
		}
		xmlHttp.onreadystatechange=(browserflag)?(serverResponse):(serverResponse());				
		//xmlHttp.onreadystatechange=serverResponse;
	       xmlHttp.open("POST",url,browserflag);
	       xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	       xmlHttp.send(queryStr);
	       xmlHttp.onreadystatechange = (browserflag)?(serverResponse):(serverResponse());
	       }else{
			   window.alert("服务器超时...");
	       }
}
function serverResponse(){
	if(4==xmlHttp.readyState){
		if(200==xmlHttp.status){
			var resData=eval("["+xmlHttp.responseText+"]");
			alert(resData[0].msg);
			if(resData[0].no!=-1){
				if(resData[0].msg=='顶成功')
					$mm('dignum').innerHTML=parseInt($mm('dignum').innerHTML)+1;
				else
					$mm('dignum').innerHTML=parseInt($mm('dignum').innerHTML)-1;
			}
		}
	}
}
window.onload = function() {
	$mm('submit').disabled = false;
	if(getCookie("author")){
	$mm('name').value=getCookie("author");
	$mm('emails').value=getCookie("email");
	$mm('websites').value=getCookie("url")?getCookie("url"):"";
	}
}
//-->