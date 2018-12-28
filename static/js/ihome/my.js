

function logout() {
    $.ajax({
        url:'/user/logout/',
        type:'DELETE',
        success:function(data) {
            if(data.code=='200') {
                location.href = '/house/index/';
            }
        }
    });
}





$(document).ready(function(){

    $.ajax({
    url:'/user/my_info/',
    data:'GET',
    dataType:'json',
    success: function(data){
                if(data.code='200'){
                    $('#user-avatar').attr('src','/static/media/'+data.user.avatar);
                    $('#user-name').html(data.user.name);
                    $('#user-mobile').text(data.user.phone);
                }
            },
            error: function(data){
                alert('failed')
            }

    })

})