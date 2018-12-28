

$(document).ready(function(){
    $.get('/house/my_auth/',function (data) {
    if(data.code== '200'){
        //已经完成实名认证
        $('#houses-list').show();
        $('.auth-warn').hide();

        for (var i=0;i<data.house_info.length;i++){
        var house = '<li>'
        house += '<a href="/house/detail/?house_id=' + data.house_info[i].id +'">'
        house += '<div class="house-title">'
        house += '<h3>房屋ID:'+data.house_info[i].id+ '—— 房屋标题'+data.house_info[i].title+'</h3>'
        house +='</div><div class="house-content">'
        house += '<img alt="" src="/static/media/' +data.house_info[i].image+'">'
        house += '<div class="house-text"><ul>'
        house += '<li>位于:' + data.house_info[i].area +'</li><li>价格：￥' +data.house_info[i].price+'/晚</li>'
        house += '<li>发布时间:'+data.house_info[i].create_time+'</li>'
        house += '</ul></div></div></a></li>'

        $('#houses-list').append(house);
        }
        }


    if(data.code=='123'){
        //未实名认证
        $('.auth-warn').show();
        $('#houses-list').hide()
    }
});
});



