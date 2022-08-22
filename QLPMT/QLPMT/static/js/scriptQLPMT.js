$(document).ready(function() {
    $("#gototop").hide()
      $("#tototop").click(function(){
        $('html, body').animate({
            scrollTop:0
        });

    });


    $(window).scroll(function() {
        if ($(this).scrollTop() >=80){
            $('nav').css({
                "position":"fixed",
                "left":0,
                "right":0,
                "z-index":9999,
                "border-radius": "0px 0px 40px 40px",
                "background-color": "white",
            })
        }
        else
            $('nav').css({
                "position":"relative",
                "left":0,
                "right":0,
                "z-index":9999,
                "background-color": "#ffffff00",
                "border-radius": "0px 0px 0px 0px"
            })




       if ($(window).scrollTop() >= 100)
            $("#gototop").show("slow")
       else
            $("#gototop").hide("slow")
    })
//    let up = document.querySelector('#gototop');
//    up.onclick = function(){
//        window.scrollTo({behavior: 'smooth',top:0});
//    }
//    var btn = $("#gototop");
//    btn.on('click', function(){
//
//        $('html, body').animate({scrollTop:0},1000);
//    });
    $("#khambenh1").click(function(){
        $(this).css({
            "background-color": "#ffffff00"
        })
    });


    $("#gototop").click(function(){
        if (".trangchu"){
            $('html, body').animate({scrollTop:0},1000);
        }
    });

    $("#gioithieu").click(function(){
        if (".trangchu"){
            $('html, body').animate({scrollTop:500},500);
        }

    });
    $("#doingubacsi").click(function(){

        $('html, body').animate({scrollTop:1000},500);
    });
     $("#dangkilichkham").click(function(){

        $('html, body').animate({scrollTop:1600},500);
    });

    $("#ThanhCong").fadeIn(function(){
        swal('Đăng kí lịch khám','Thành công','success')
    })
    $("#DaDuNguoi").fadeIn(function(){
        swal('Đã đủ bệnh nhân','Đăng kí vào hôm sau. Xin cảm ơn','error');
    })
    $("#TKKTT").fadeIn(function(){
        swal('Người dùng không tồn tại','Hãy kiểm tra lại thông tin','error');
    })



})
$(window).on('load',function(event){
    $('body').removeClass('preload')
    $('.load').delay(300).fadeOut('fast');
})




