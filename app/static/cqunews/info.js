var html = $(".mainbody").html();
//console.log(typeof(html))
fhtml = html.replace(/&lt;/g,"<").replace(/&gt;/g,">");

$(".mainbody").html(fhtml);
