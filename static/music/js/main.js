/*! CL's Music Player - 2016-07-16
* https://music.caoliang.net
* Copyright (c) 2016 */
$(function(){
    var player_status = "pause";
    var times_server = 0;
    var server_id = 0;
    var lst_cnt = 0;
    var current_song = 0;
    var msc_name = "";
    var pgs = [" ", " ·", " · ·", " · · ·"];
    var pgsblock_pos_x = 0;
    var pgs_lock = false;
    var frend_link_status = false;
    var friend_link_task_id = 0;
    var list_touch_start = 0;
    if (!window.CDN_URL){window.CDN_URL = ""};
    var pauseImgPos = window.CDN_URL + "/static/music/player/pause.png",
        playImgPos = window.CDN_URL + "/static/music/player/play.png",
        musicFileFolder = window.CDN_URL + "/music_file/",
        hxjjImgLocation = "url('"+ window.CDN_URL + "/static/music/friend_link/hxjj.jpg')";

    function setCookie(cname, cvalue, exdays) {
        window.localStorage.setItem(cname, cvalue)
    }
    function getCookie(cname) {
        return window.localStorage.getItem(cname) || "";
    }
    function obvious(){
        document.getElementById("btn_play").style.cursor="pointer";
        $("#btn_play").animate({opacity:'0.7'},200);
    }
    function unobvious(){
        $("#btn_play").animate({opacity:'1'},300);
    }
    function display_list(){
        /* 先设置到一个合适的位置 */
        if(current_song>3){
            var ht = ((-20)*current_song + 35) + "px";
            $("#msc_list").animate({marginTop:ht});
        }else{
            $("#msc_list").animate({marginTop:"0px"});
        }
        $("#first_layer").fadeOut(0);
        $("#second_layer").fadeIn();
    }
    function back_to_first_layer(){
        $("#second_layer").fadeOut(0);
        $("#first_layer").fadeIn();
    }
    function page_up(distance){
        if(!arguments[0]) distance = 80;

        var h = $("#msc_list").css("margin-top");
        var ht_s = Number(h.substring(0,h.length -2));
        if(ht_s < 0){
            var ht = (ht_s + distance) + "px";
        }else{
            ht="0px";
        }
        $("#msc_list").clearQueue();
        $("#msc_list").animate({marginTop:ht});

    }
    function page_down(distance){
        if(!arguments[0]) distance = 80;

        var h = $("#msc_list").css("margin-top");
        var ht_s = Number(h.substring(0,h.length -2));

        /* 当列表长度在范围之内 才滚动 */
        if(ht_s > ((lst_cnt -5)*(-20))){
            var ht = (ht_s - distance) + "px";

            $("#msc_list").clearQueue();
            $("#msc_list").animate({marginTop:ht});
        }
    }
    function touch_list(offset){

        var h = $("#msc_list").css("margin-top");
        var ht_s = Number(h.substring(0,h.length -2));
        var ht = (ht_s + offset) + "px";

        var top_border = 0;
        var bottom_border = (lst_cnt -5)*(-20);

        if(ht_s < bottom_border){
            var ht = bottom_border + "px";
        }
        if(ht_s > top_border){
            var ht = top_border + "px";
        }

        $("#msc_list").css("margin-top",ht);
    }
    function scrolllist(){
        var event = window.event;
        event.preventDefault();

        if(event.wheelDelta>0){
            page_up(60);
        }else{
            page_down(60);
        }
    }
    function move_pgsblock(){
        pgs_lock = true;
    }
    function player_server(){
        times_server += 1;
        document.getElementById("music_name").innerHTML = "播放：" + msc_name + pgs[times_server%4];

        var audio = document.getElementById("audio");

        if(pgs_lock == false){
            /* 百分比 255px 滑块到最右端 */
            var pstage = audio.currentTime * (255 / audio.duration);
            document.getElementById("pgs_block").style.left = pstage.toString() +"px";
        }else{

            var x_s = document.getElementById("pgs_block").style.left;
            var x = Number(x_s.substring(0,x_s.length -2));

            audio.currentTime = Number(x / 255 * audio.duration);
            pgs_lock = false;
        }

        if((times_server % 5) ==0){
            setCookie("player_time",audio.currentTime,30);
        }
    }
    function toggle_play(){
        if(player_status == "play"){
            /* to stop music */
            player_status = "pause";
            setCookie("player_status","pause",30);

            $("#btn_play").attr("src", playImgPos);
            $("#music_name")[0].innerHTML = "暂停：" + msc_name;
            if(server_id != 0){
                clearInterval(server_id);
                server_id = 0;
            }

            $("#audio").animate({volume:'0'},1000);
            setTimeout("$('#audio')[0].pause()",1000);
        }else{
            player_status = "play";
            setCookie("player_status","play",30);

            $("#btn_play").attr("src", pauseImgPos);

            $('#audio')[0].play();
            if(server_id == 0){
                server_id = setInterval(player_server,1000);
            }

            $("#audio").animate({volume:'1'},1400);
        }
    }
    function play_by_list(the_song){
        play_access(the_song.id.substr("music_list_".length));
    }
    function play_next(){
        var song_index = (current_song + 1)%(lst_cnt);
        play_access(song_index);
    }
    function play_access(index,time){
        if(!arguments[1]){time = 0;}
        index = Number(index);
        if (music_list.length < index){index = 0};
        current_song = index;
        msc_name = music_list[index].substring(0,music_list[index].length-4);

        $("#msc_list").find("a").each(function(){
            $(this).css("color","");
        });
        $("#msc_list").find("a").eq(index).css("color","red");

        back_to_first_layer();

        $("#audio")[0].src = musicFileFolder + music_list[index];
        if(time != 0){$("#audio")[0].currentTime = time;};


        if(server_id == 0){
            server_id = setInterval(player_server,1000);
        }
        $("#audio")[0].volume = 0;
        $("#audio")[0].play();
        $("#audio").animate({volume:'1'},1400);
        $("#btn_play").attr("src", pauseImgPos);
        player_status = "play";

        setCookie("player_index",Number(current_song),30);
    }
    function generate_music_list_dom(){
        for (i in music_list) {
            $('<a/>', {
                html: music_list[i].substring(0,music_list[i].length-4),
                id: "music_list_" + i,
                click: function(){play_by_list(this);},
            }).appendTo($('#msc_list'));
            $('<br />').appendTo($('#msc_list'));
        }
    }
    function friend_link_server(){
        if (frend_link_status == false){
            frend_link_status = true;

            $("#friend_link_p").animate({"opacity":"0.0"},1000);
            setTimeout(function(){
                $(".hxjj").css({
                    "background-image": hxjjImgLocation,
                    "opacity": "0"
                });
                $(".hxjj").animate({"opacity":"1.0"}, 1000);
            },1000);
        }else{
            frend_link_status = false;

            $(".hxjj").animate({"opacity":"0.0"},1000);
            setTimeout('$(".hxjj").css({"background-image":""});$("#friend_link_p, .hxjj").animate({"opacity":"1.0"},1000);',1000);
        }
    }
    function prepare_friend_link(){
        if (current_song == 1){
            if(friend_link_task_id == 0){
                $("#friend_link_p").css("cursor","pointer");
                $("#friend_link_p, #music_name").bind("click",function(){
                    if(player_status == "play"){toggle_play();}
                    window.open("http://www.phantasm-kekkai.com/");
                });
                friend_link_task_id = setInterval(function(){friend_link_server()}, 5500);
            }
        }else{
            if(friend_link_task_id != 0){
                $("#friend_link_p").css("cursor","default");
                $("#friend_link_p, #music_name").unbind("click");

                clearInterval(friend_link_task_id);
                friend_link_task_id = 0;
            }

            if (frend_link_status == true){
                frend_link_status = false;
                $("#friend_link_p, .hxjj").animate({"opacity":"0.0"},1000);
                setTimeout('$(".hxjj").css({"background-image":""});$("#friend_link_p, .hxjj").animate({"opacity":"1.0"},1000);',1000);
            }
        }
    }

    /* global variables init */
    lst_cnt = music_list.length;
    /* Dom init */
    generate_music_list_dom();
    $("body").fadeIn(500);
    pgsblock_pos_x = Number($("#pgs_block").offset().left);
    /* bind event */
    document.getElementById("pgs_block").addEventListener('touchmove', function(event) {
        if (event.targetTouches.length == 1) {
    　　　　 event.preventDefault();

            var touch = event.targetTouches[0];
            var offset = touch.clientX - pgsblock_pos_x;
            if(offset < 0){
                offset = 0;
            }
            if(offset > 255){
                offset = 255;
            }
            pgs_lock = true;
            document.getElementById("pgs_block").style.left = offset + "px";         
        }
    }, false);
    $("#btn_play").bind("mouseover",function(){obvious();}).bind("mouseout",function(){unobvious();}).bind("click",function(){toggle_play();});
    $("#pgs_block").bind("mouseover",function(){$("#pgs_block").css("cursor","pointer");}).draggable({ containment: "parent" }).mousedown(function(){move_pgsblock();});
    $("#music_play_next_btn").click(function(){play_next();});
    $("#music_list_btn").click(function(){display_list();});
    $("#btn_up").click(function(){page_up();});
    $("#btn_back").click(function(){back_to_first_layer();});
    $("#btn_down").click(function(){page_down();});
    $("#msc_list_border").bind('mousewheel',function(){scrolllist();});    
    $("#audio").bind('ended',function(){play_next();}).bind('play',function(){prepare_friend_link();});
    $(document).keydown(function(event){if(event.keyCode == 32){toggle_play()}});

    player_status = getCookie("player_status");
    if(player_status == ""){
        setCookie("player_status","play",30);
        player_status = "play";
    }
    var time = getCookie("player_time");
    if(time == ""){
        setCookie("player_time",0,30);
        time = 0;
    }
    var index = getCookie("player_index");
    if(index == ""){
        setCookie("player_index", 0, 30);
        index = 0;
    }

    current_song = index;

    if(player_status == "pause"){
        $("#btn_play").attr("src", playImgPos);
        if (music_list.length < index){index = 0}
        msc_name = music_list[index].substring(0, music_list[index].length - 4);
        $("#music_name")[0].innerHTML = "暂停：" + msc_name;
        $("#msc_list").find("a").each(function(){$(this).css("color","");});
        $("#msc_list").find("a").eq(index).css("color","red");
        $("#audio")[0].src = musicFileFolder + music_list[index];
    }else{
        play_access(index,time);
    }
});
