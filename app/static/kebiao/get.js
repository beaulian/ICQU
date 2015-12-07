//var data=0;
//var wdata=[];
var mydate=new Date();
var week_t;
var dates=0;

//cal1()
calweek();
// request1();
$('#submit').click(function(e){
		if ($('#SID').val() == '') 
 			alert("请输入学号!");
 		else if ($('#password').val() == '')
 			alert("请输入密码!");
 		else
 		{
 			$.cookie("student", $("#SID").val(), {expires: 1});
			$.cookie("password", $("#password").val(), {expires: 1});
			$("#divform").css("display", "none");
			$("#content").css("display", "block");
			window.location.reload();
		}
});
if ($.cookie("student") != undefined) {
	$("#divform").css("display", "none");
	$("#content").css("display", "block");
	request1();
}
/*function cal1()
{
	for(var h=0;h<19;h++)
{
    wdata[h]=new Array();
    for(var i=0;i<7;i++)
    {
        wdata[h][i]=new Array();
        for(var j=0;j<5;j++)
        {
            wdata[h][i][j]='';
        }
    }
}

}*/
function calweek()
{
	var date_json = {1:31,2:28,3:31,4:30,5:31,6:31,7:31,8:31,9:30,10:31,11:30,12:31};
	for(var i=9;i<mydate.getMonth()+1;i++)
		dates+=date_json[i];
	dates+=mydate.getDate();
	week_t=parseInt(dates/7);
	console.log(week_t);
}


/*function handle()
{
	for (var i = 0; i < data['任课老师'].length; i++)
	{
		for(var h = 0; h < 19; h++)
		{
			if (data['周次'][i][h])
			{
				wdata[h][parseInt(data['时间'][i][0]) - 1][(parseInt(data['时间'][i][1]) + 1) / 2 - 1] = data['课程'][i] + " " + data['地点'][i] + " " + data['任课老师'][i];
			}
		}
	}
}*/


function settable()
{
	$("#form").text("");
    var g=document.all.select_t.value-1;
    var tb="<tr>"+
            "<td>星期</td>"+
            "<td>星期一</td>"+
            "<td>星期二</td>"+
            "<td>星期三</td>"+
            "<td>星期四</td>"+
            "<td>星期五</td>"+
			"<td>星期六</td>"+
			"<td>星期天</td>"+
            "</tr>";
	var str='<tr><th colspan=8>第'+(g+1)+'周</th>'+tb;
	var week = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"];
	var class1=["1-2节","3-4节","5-6节","7-8节","9-11节"];
	for(var i=0;i<5;i++)
	{
		str+="<tr><td>" + class1[i] + "</td><td>" + wdata[g][0][i] + "</td>" +
		"<td>" + wdata[g][1][i] + "</td>" +
		"<td>" + wdata[g][2][i] + "</td>" +
		"<td>" + wdata[g][3][i] + "</td>" +
		"<td>" + wdata[g][4][i] + "</td>" +
		"<td>" + wdata[g][5][i] + "</td>" +
		"<td>" + wdata[g][6][i] + "</td>"+ "</tr>";
	}
	$("#form").append(str);
}
function setselect()
{
	var str_select="<select id='week' onchange="+"settable()"+" name=select_t>";
	for(var i=1;i<20;i++)
	{
		if(i==week_t)
			str_select+="<option selected="+"selected"+" value="+i+">第"+i+"周(当前周)</option>";
		else
			str_select+="<option"+" value="+i+">第"+i+"周</option>";
	}
	$("#div_t").append(str_select+"</select>");
}

function request1() {
    var xhr = new XMLHttpRequest();
    xhr.onload = function ()
    {
        if ((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304)
        {
            wdata=eval('('+xhr.responseText+')');
			if(!wdata[0])
			{
				$("#tit").text("");
				$("#div_t").append("<h3 align=center>用户名或密码错误</h3>");
				
			}
			else
			{
				//handle();
				setselect();
				settable();
			}
        }
        else
        {
            alert("try again");
        }
    }
    var url = "/form?"+$.cookie('student')+"||"+$.cookie('password');
    xhr.open('get', url, false); // synchronous
	xhr.send(null);
};
