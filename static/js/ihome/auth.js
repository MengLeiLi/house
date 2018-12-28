function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


$(document).ready(function(){
    $.get('/user/auths/',function(data){
    $('#real-name').val(data.id_name)
    $('#id-card').val(data.id_card)
    if(data.id_name!=null && data.id_card!= ''){
        $('.btn-success').hide()
        $('#real-name').attr('disabled','disabled');
        $('#id-card').attr('disabled','disabled');

    }

    });
    $('#form-auth').submit(function(){
        $.ajax({
            url:'/user/auths/',
            type:'POST',
            data:{
                id_name:$('#real-name').val(),
                id_card:$('#id-card').val()

            },
            dataType:'json',
            success:function(data){
            if(data.code=='200'){
                $('.btn-success').hide();
                $('.error-msg').hide();

            }else{
            $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>'+data.msg);
            $('.error-msg').show();

            }

            }
        });
    });

})
