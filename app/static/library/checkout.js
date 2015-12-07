function nnowborrow(){
    $("#nowborrows").css("display","block");
    $("#outdateinfos").css("display","none");
    $("#readers").css("display","none");
    $("#readingbooks").css("display","none");
    $(".nb").empty();
    $(".em").empty();
    if (nowborrow["statusinfo"] == "none"){
        $("#nowborrows").html("<p align='center'>没有相关记录!</p>")
    }else{
    $("#nowborrows").append("<em style='float:left' class='em'>" + 
            "当前你已借阅图书<font class='redfont'>" + nowborrow["alreadyBorrow"] +
	    "</font>册, 当前借阅<font class='redfont'>" + nowborrow["currentBorrow"] + 
            "</font>册，已还未评论图书<font class='redfont'> " + nowborrow["notComment"] +
            "</font>册，总共可以借阅图书<font class='redfont'>" + nowborrow["sumBorrow"] +
            "</font>册。</em>"
            )
        // console.log(nowborrow["alreadyBorrow"]);
        for (var i=1; i<=parseInt(nowborrow["currentBorrow"]); i++){
            bookorder = nowborrow["book_"+ i.toString()];
            // console.log(bookorder);
            //console.log(bookorder.状态.split("/"));
            //console.log(bookorder.状态.split("/")[5]);
            $("#nowb").append(
                    // console.log(bookorder);
                    "<tr class='nb'>" + 
                    "<td class='primary'>" + "<img src='/static/library/images/" + bookorder["状态"].split("/")[5] + "' align='absmiddle' />" + "</td>" +
                    "<td class='primary'>" + bookorder["题名"][1] + "</td>" +
                    "<td class='primary'>" + bookorder["索书号"] + "</td>" +
                    "<td class='primary'>" + bookorder["馆藏地"] + "</td>" + 
                    "<td class='primary'>" + bookorder["续借次数"] + 
                    "<td class='primary'>" + bookorder["借阅时间"] + "/" + bookorder["应还时间"] + "</td>" +
                    "<td class='primary'>" + "<input type='button' value='续借' style='width:4em;height:3em;' class='btn-sm btn-info' onclick=" + bookorder["续借"]  + " /> " + "</td></tr>" 
            )

        }
    }
}


function readingbook(){
    $("#nowborrows").css("display","none");
    $("#outdateinfos").css("display","none");
    $("#readers").css("display","none");
    $("#readingbooks").css("display","block");
    $(".rb").empty();
    if (readbookings["statusinfo"] == "none"){
        $("#readingbooks").html("<p align='center'>没有相关记录!</p>")
    }else{
    for (var i=1; i<=parseInt(readbookings.count_book); i++){
        bookorder = readbookings["book_"+ i.toString()]
        //console.log(bookorder);
        $("#readb").append(
                "<tr class='rb'>" + 
                "<td class='primary'>" + "<img src='/static/library/images/" + bookorder.状态.split("/")[5] + "' align='absmiddle' />" + "</td>" +
                "<td class='primary'>" + bookorder.题名[1] + "</td>" +
                "<td class='primary'>" + bookorder.索书号 + "</td>" +
                "<td class='primary'>" + bookorder.预约时间 + "</td>" +
                "<td class='primary'>" + bookorder.通知时间 + "</td>" +
                "<td class='primary'>" + bookorder.前面还有几位 + "</td></tr>"
                
            )

        }
    }
}


function outdateinfo(){
    $("#nowborrows").css("display","none");
    $("#outdateinfos").css("display","block");
    $("#readers").css("display","none");
    $("#readingbooks").css("display","none");
    $(".ob").empty();
    if (outdateinfos["statusinfo"] == "none"){
        $("#outdateinfos").html("<p align='center'>没有相关记录!</p>")
    }else{
    for (var i=1; i<=parseInt(outdateinfos.count_book); i++){
        bookorder = outdateinfos["book_"+ i.toString()]
        // console.log(bookorder.超期天数);
        $("#outdi").append(
                "<tr class='ob'>" + 
                "<td class='primary'>" + "<img src='/static/library/images/" + bookorder.状态.split("/")[5] + "' align='absmiddle' />" + "</td>" +
                "<td class='primary'>" + bookorder.题名[1] + "</td>" +
                "<td class='primary'>" + bookorder.馆藏地 + "</td>" +
                "<td class='primary'>" + bookorder.超期天数 + "</td>" + 
                "<td class='primary'>" + bookorder.借出时间 + "/" + bookorder.应还时间 + "</td>" +
                "<td class='primary'>" + bookorder.归还时间 + "</td></tr>"

            )
        }
    }
}

function reader(){
    $("#nowborrows").css("display","none");
    $("#outdateinfos").css("display","none");
    $("#readers").css("display","block");
    $("#readingbooks").css("display","none");
    $(".rd").empty();
    $(".span").empty();
    if (readers["statusinfo"] == "none"){
        $("#readers").html("<p align='center'>没有相关记录!</p>")
    }else{
    $(".span").html("总欠款金额：" + readers.sumMoney + "元");
    for (var i=1; i<=parseInt(readers.count_book); i++){
        bookorder = readers["book_"+ i.toString()]
        //console.log(bookorder);
        $("#res").append(
                "<tr class='rd'>" + 
                "<td class='primary' width='20%'>" + bookorder.欠款时间+ "</td>" +
                "<td class='primary' width='20%'>" + bookorder.欠款金额 + "</td>" +
                "<td class='primary' width='60%'>" + bookorder.原因 + "</td></tr>"

            )
        }
    }   
}
