
$('#submit').click(function(e){
		if ($('#SID').val() == '') 
 			alert("请输入学号!");
 		else if ($('#password').val() == '')
 			alert("请输入密码!");
 		else
 		{
			$.cookie("studentl", $("#SID").val(), {expires: 1});
			$.cookie("passwordl", $("#password").val(), {expires: 1});
			$("#sform").css("display","none");
		    $("#library").css("display","block");
			window.location.reload();
		}
});
if ($.cookie("studentl") != undefined) {
	$("#sform").css("display","none");
	$("#library").css("display","block");
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
    			nowborrow = data["NowBorrow"];
        		readbookings = data["ReadBooking"];
        		outdateinfos = data["OutDateInfo"];
        		readers = data["ReaderArrearage"];
        		// console.log(outdateinfos);
				nnowborrow();
    		}
    		
        }
        else
        {
            alert("try again");
        }
    }
    var url = "/library?SID="+$.cookie('studentl')+"&password="+$.cookie('passwordl');
    xhr.open('get', url, false); // synchronous
	xhr.send(null);
};





