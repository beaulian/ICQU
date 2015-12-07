function goNext(count){
	value = document.getElementById("pnumber").innerHTML;
	//console.log((parseInt(value)+1).toString());
	//console.log(value);
	goPage(parseInt(value)+1,count);
	//console.log(document.getElementById("number").value);
}

function goPage(pagenumber,count){
	if (pagenumber < 1);
	else{
		sum = Math.floor(parseInt(count)/10);
		//console.log(sum);
		if (pagenumber > sum);
		else{
			window.location.href=pagenumber.toString();
		}
	}
}

function goAgo(){
	value = document.getElementById("pnumber").innerHTML;
	goPage_two(parseInt(value)-1);
}

function goPage_two(pagenumber){
	if (pagenumber == -1);
	else window.location.href=pagenumber.toString();
}
