$('#submit').click(function(e){
		if ($('#SID').val() == '') 
 			alert("请输入学号!");
 		else if ($('#password').val() == '')
 			alert("请输入密码!");
 		else
 		{
			$.cookie("studenty", $("#SID").val(), {expires: 1});
			$.cookie("passwordy", $("#password").val(), {expires: 1});
			$(".sform").css("display", "none");
			$(".yikatong").css("display", "block");
			window.location.reload();
		}
});
if ($.cookie("studenty") != undefined) {
	$(".sform").css("display", "none");
	$(".yikatong").css("display", "block");
	request1();
}


function request1() {
    var xhr = new XMLHttpRequest();
    xhr.onload = function ()
    {
        if ((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304)
        {
            data=eval('('+xhr.responseText+')');
			if (data.errcode == 1 && data.errmsg == "wrong_id"){
    			$("#body").html("<div align=center>帐号或密码输入有误,请重新输入!</div>")
    		}
    		else{
    			// $(".sform").css("display","none");
       //  		$(".yikatong").css("display","block");
				$("#yue").html(data[0]);
				//$("#booknum").html(data[1]);
				$("#overflow").html(data[1]);
    		}
    		
        }
        else
        {
            alert("try again");
        }
    }
    var url = "/yikatong?SID="+$.cookie('studenty')+"&password="+$.cookie('passwordy');
    xhr.open('get', url, false); // synchronous
	xhr.send(null);
};


