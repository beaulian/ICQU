$('#submit').click(function(e){
		if ($('#SID').val() == '') 
 			alert("请输入学号!");
 		else if ($('#password').val() == '')
 			alert("请输入密码!");
 		else if ($("#xueqi").val() == '')
 			alert("请选择学年学期!");
 		else
 		{
 			var select = $("#xueqi").val();
 			var year = select.split("-")[0];
		 	var team_number = select.split("-")[1];
			$.cookie("studentg", $("#SID").val(), {expires: 1});
			$.cookie("passwordg", $("#password").val(), {expires: 1});
			$.cookie('year', year, {expires: 1});
			$.cookie('team_number', team_number, {expires: 1});
			$("#divform").css("display","none");
		 	$("#content_menu").css("display","block");
			window.location.reload();
		}
});
if ($.cookie("studentg") != undefined) {
	$("#divform").css("display","none");
	$("#content_menu").css("display","block");
	request1();
}


function request1() {
    var xhr = new XMLHttpRequest();
    xhr.onload = function ()
    {
        if ((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304)
        {
            data=eval('('+xhr.responseText+')');
			if (data.errcode && data.errcode == 1){
		 	  		if (data.errmsg == "wrong SID or password"){
	                	$("#body").html("<div align=center>帐号或密码输入有误,请重新输入!</div>")
	                }
	                else if (data.errmsg == "cannot search"){
	                	$("#body").html("<div align=center>成绩无法查询,请登录教务网查看原因!</div>")
	                }										
		 	  	}else{
			 	 //  	$("#divform").css("display","none");
		 			// $("#content_menu").css("display","block");
			 	    grade_info = data;
			 	    grade();
		 	  	}
    		
        }
        else
        {
            alert("try again");
        }
    }
    var url = "/getgrade?SID="+$.cookie('studentg')+"&password="+$.cookie('passwordg')+
    									"&year="+$.cookie('year')+"&team_number="+$.cookie('team_number');
    xhr.open('get', url, false); // synchronous
	xhr.send(null);
}; 


function grade () {
	count = grade_info.课程总数;
	$(".tishi").html(grade_info.学年学期);
	for (var j=0; j<count; j++){
		var tr = "<tr class='tr' align='center'>" +
				"<td class='order section' width='20%'>" + (j+1).toString() + "</td>" +
				"<td class='my subject' width='40%'>" + grade_info.课程名称[j].split("]")[1] + "</td>" +
				"<td class='my credit{2}' width='20%'>" + grade_info.学分[j] +"</td>" +
				"<td class='my grade{3}' width='20%'>" + grade_info.成绩[j] + "</td>" +
			"</tr>"
		// String.format();
		// minetr = String.format(tr, i,i,i,i);
		$("table#day").append(tr);
	}
	//console.log(count);
	// for (var j=0; j<count; j++){
	// 	order = j+1;
	// 	$(".section" + order).append(order.toString());
	// 	$(".subject" + order).append(grade_info.课程名称[j].split("]")[1]);
	// 	$(".credit" + order).append(grade_info.学分[j]);
	// 	$(".grade" + order).append(grade_info.成绩[j]);
	// }
}



 

