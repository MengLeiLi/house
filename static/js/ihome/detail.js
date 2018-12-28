function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    $(".book-house").show();

    var search_url = document.location.search
    house_id = search_url.split('=')[1]
    $.get('/house/detail/'+house_id+'/',function(data){
    console.log(data)
    if (data.code=='200'){
    for (var i=0;i<data.house.images.length;i++){
        var swiper_li ='<li class="swiper-slide"><img src="/static/media/"'
        $('.swipder-warpper').append(swiper_li)

    }
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    $('.house-price').html('￥<span>'+data.house.price+'</span>/晚')

    $('.house-info-address').html(data.house.address)

    $('.house-title').html(data.house.title)

    $('.landlord-name').html('房东:<span>'+data.house.user_name+'</span>')

    $('.landlord-pic').html('<img src="/static/media/'+data.house.user_avatar+'">')

    $('.house-type-detail').html('<h3>出租'+data.house.room_count+'</h3>'+'<p>'+data.house.acreage+'</p>'+'<p>'+data.house.unit+'</p>')

    $('.house-capacity').html('<h3>宜住'+data.house.capacity+'</h3>')

    $('house-bed').html('<h3>卧床配置</h3><p>'+data.house.beds+'</p>')

    var house_info_style = '<li>收取押金<span>'+data.house.deposit+'</span></li>'
    house_info_style += '<li>最少入住天数<span>'+data.house.min_days+'</span></li>'
    house_info_style += '<li>最多入住天数<span>'+data.house.max_days+'</span></li>'
    $('.house-info-style').html(house_info_style)
    var house_facility_list = ''
    for(var i=0;i<data.facility_list.length;i++){
        house_facility_list += '<li><span class="'+data.facility.css+'"></span>'+data.facility.name+'</li>'


         }
        $('.house-facility-list').html(house_facility_list)
        $('.book-house').attr('href','/order/booking/?id='+data.house.id)

        if(data.booking==1){

        $('.book-house').show();
        }else{
        $('.book-house').hide();
        }



    }
    })
})