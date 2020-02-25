$(function(){
	clearLeft();clearBorder();clearContnt();//reName();
$('[data-type="checkbox"]').click(function(){  
var data_value = $(this).attr('data-value'),  
txtalso = $.trim($(".txtValue").val());  
if($(this).prop("checked")) {  
if(txtalso.length > 0) {  
if(txtalso.indexOf(data_value+',') != -1) {  
return ;  
} else {  
txtalso += data_value + ',';  
}  
} else {  
txtalso = data_value+',';  
}  
} else {  
if(txtalso.indexOf(data_value+',') != -1) {  
txtalso = txtalso.replace(data_value+',', '');  
}
if(txtalso.indexOf(data_value) != -1){
txtalso = txtalso.replace(data_value, '')}  
}  
$(".txtValue").val(txtalso);
$(".txtValue").attr("value",txtalso);
});
$(".txtValue").unbind("keyup").bind("keyup",function () {
	console.log("upupupup.....")
	txtalso = $.trim($(".txtValue").val());
	$(".txtValue").attr("value",txtalso);
});
$('[data-type="checkall"]').click(function(){  
var str = '';  
if($(this).prop("checked")) {  
$.each($('[data-type="checkbox"]'), function(i){  
str += $(this).attr('data-value') + ',';  
});  
$('[data-type="checkbox"]').prop('checked', true);  
} else {  
$('[data-type="checkbox"]').prop('checked', false);  
}  
$(".txtValue").val(str);
$(".txtValue").attr("value",txtalso);
}); 
$(".txtValue").keyup(function(ev){//key:"Backspace"keyCode:8
	console.log(ev);
	if(ev.key=="Backspace"&&ev.keyCode==8){
		checkText();
	}
  $(".txtValue").css("background-color","#D6D6FF");
});
});
function clearLeft() {
		$("td").css("padding-left",0);
    }
function  clearBorder() {
	$("td").css("border",0);
}
function reName() {
	$("label[for='id_column']").html("栏目");
}
function clearContnt() {
	var text=$(".txtValue");
	var value=text.val();
	value=value.replace('/','');
	text.val(value);
	text.attr("value",value);
}
function checkText(){
	txtalso = $.trim($(".txtValue").val()); 
	//textArray=txtalso.split(',');
	
	$.each($('[data-type="checkbox"]'), function(i){  
	console.log($(this).attr('data-value'));
	if(txtalso.indexOf($(this).attr('data-value'))<0){
			$(this).prop('checked', false);
		}
});

} 