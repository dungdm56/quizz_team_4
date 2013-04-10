function start(){
	setup(document.forms["form1"].time2.value,"form1");
	repeat()
}

start();

function repeat() {
	down("form1");
	setTimeout("repeat()",1000);
}

function setup(time,box){
	document.forms[box].time2.value=time;
}

function down(box){
	document.forms[box].time2.value = document.forms[box].time2.value*60 - 1;
	time = document.forms[box].time2.value;
	mins = (time - (time % 60)) / 60;
	time = time - (mins * 60);
	secs = time;
	if(mins < 10) out = out+"0";
	out = out+mins+":";
	if(secs < 10) out = out+"0";
	out = out+secs;
	if(mins+secs> 1) document.forms[box].time.value = out;
	else document.forms[box].time.value = ("Time out !");
}