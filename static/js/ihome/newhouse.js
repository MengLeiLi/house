function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
//    $.ajax(function(){
//    url:'/house/new_house',
//    data:'GET',
//    dataType:json,
//
//
//    })

    $.get('/house/area_facility/',function(data){

    var area_html =''
    for (var i=0;i<data.area.length;i++){
        area_html += '<option value="'+ data.area[i].id + '">' + data.area[i].name + '</option>'
        }
        $('#area-id').html(area_html);


    var facility_html_list = ''
        for(var i=0; i<data.facility.length; i++){
            var facility_html = '<li><div class="checkbox"><label><input type="checkbox" name="facility"'
            facility_html += ' value="' + data.facility[i].id + '">' + data.facility[i].name
            facility_html += '</label></div></li>'

            facility_html_list += facility_html
        }
        $('.house-facility-list').html(facility_html_list);

     })
     $('#form-house-info').submit(function () {
        $('.error-msg text-center').hide();
        $.post('/house/new_house/',$(this).serialize(),function (data) {
            if(data.code== '200'){
                $('#form-house-info').hide();
                $('#form-house-image').show();
                $('#house-id').val(data.house_id);
            }else{
                $('.error-msg text-center').show().find('span').html(ret_map[data.code]);
            }
        });
        return false;
    });
    $('#form-house-image').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/house/image_house/',
        type:'POST',
        dataType:'json',
        success:function(data){
            if(data.code=='200'){
                $('.house-image-cons').append('<img src="/static/media/'+data.f1_filename+'"/>');

            }

        }

    })


    })






})