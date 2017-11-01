$(function(){
	$('#search').click(function(){
	url_token = $('#url_token').val()
	if (url_token == ""){
		alert('请输入url_token');
		return false;    // 要返回false避免页面重新刷新
	} else {
		window.location.href = '/relation.html?url_token='+url_token;
		console.log(window.location.href);
		return false;
	}
})
})
