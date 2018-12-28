function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {

        $('#form-avatar').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/user/profile/',
            type: 'POST',
            dataType: 'json',
            success:function(data){
                if (data.code == '200'){
                    $('#user-avatar').attr('src','/static/media/'+data.avatar);

                }
            },
            error:function(data){

            }
            })
        });








    $('#form-name').submit(function (e) {
        e.preventDefault();
        var name = $('#user-name').val();
        $.ajax({
            url:'/user/profile/',
            type:'POST',
            data:{'name':name},
            success:function (data) {
                if(data.code== '200'){
                    showSuccessMsg();
                }else{
                    $('.error_msg2').html('<i class="fa fa-exclamation-circle"></i>' +data.msg);
                    $('.error_msg2').show();
                }
            }
        });
        return false;
    });
})



