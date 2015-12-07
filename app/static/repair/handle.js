var wdata;
function setweb(wdata)
{
	for(i in wdata)
	{
		if((i=="xueyuan"||i=="loudong"||i=="chuangwei")&&wdata[i])
		{
			$("#"+i).val(wdata[i]);
			$("#"+i).attr({disabled:"disabled"});
		}
		else if(wdata[i])
		{
			$("#"+i).attr({disabled:"disabled",value:wdata[i]});
		}
	}
	$("#sform").css("display", "none");
	$("#whole").css("display", "block");
}
$('#submit').click(function(e){
		if ($('#SID').val() == '') 
 			$("#error").html("<span style='color:red'>请输入学号!</span>");
 		else if ($('#password').val() == '')
 			$('#error').html("<span style='color:red'>请输入密码!</span>");
 		else
 		{
			$.cookie("studentw", $("#SID").val(), {expires: 1});
			$.cookie("passwordw", $("#password").val(), {expires: 1});
			$("#sform").css("display", "none");
			$("#whole").css("display", "block");
			window.location.reload();
		}
});
if ($.cookie("studentw") != null) {
	request1();
}
function handle_data(wdata)
{
	var dic1={};
	for(i in wdata)
	{
		if(!wdata[i])
		{
			wdata[i]=$("#"+i).val();
		}
	}
	var str1="";
	for(i in wdata)
	{
		str1+=i+"="+wdata[i]+"&";
	}
	return str1;
}

function request1() {
    var xhr = new XMLHttpRequest();
    xhr.onload = function ()
    {
        if ((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304)
        {
            wdata=eval('('+xhr.responseText+')');
			if(wdata["status"]=="0")
			{
				$("#whole").text("");
				$("#whole").append("<h3 align=center>用户名或密码错误</h3>");
			}
			else
				setweb(wdata["content"]);
        }
        else
        {
            alert("try again");
        }
    }
    var url = "/login?"+$.cookie('studentw')+"||"+$.cookie('passwordw');
    xhr.open('get', url, false); // synchronous
	xhr.send(null);
};


function tijiao()
{
	var xhr = new XMLHttpRequest();
	var str2=handle_data(wdata["content"])+"cookie="+wdata["cookie"];
	xhr.open("post","/tijiao");
	xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	xhr.send(str2);
	xhr.onload=function()
	{
		var tdata=eval('('+xhr.responseText+')');
		if(tdata["status"]=="1")
		{
			$("#whole").text("");
			$("#whole").append("<h3 align=center>不能重复报修</h3>");
		}
		else
		{
			str_t="<h3>报修成功</h3>"
			$("#whole").text("");
			$("#whole").append(str_t+tdata["content"]);
		}
		
	}
}



