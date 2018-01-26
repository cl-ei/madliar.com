$(function(){
    $.fn.shuffleLetters = function(prop){
		var options = $.extend({
			"step"		: 15,			// How many times should the letters be changed
			"fps"		: 15,			// Frames Per Second
			"text"		: "", 			// Use this text instead of the contents
			"callback"	: function(){}	// Run once the animation is complete
		},prop);
		return this.each(function(){
			var el = $(this),
				str = "";

			if(el.data('animated')){
				return true;
			}else{
			    el.data('animated',true);
            }
			if(options.text) {
				str = options.text.split('');
			}else {
				str = el.text().split('');
			}

			var types = [],
				letters = [];
			for(var i=0;i<str.length;i++){
				var ch = str[i];
				if(ch == " "){
					types[i] = "space";
					continue;
				}else if(/[a-z]/.test(ch)){
					types[i] = "lowerLetter";
				}else if(/[A-Z]/.test(ch)){
					types[i] = "upperLetter";
				}else {
					types[i] = "symbol";
				}
				letters.push(i);
			}
			el.html("");
			(function shuffle(start){
				var i,
					len = letters.length,
					strCopy = str.slice(0);	 // Fresh copy of the string

				if(start>len){
					el.data('animated',false);
					options.callback(el);
					return;
				}
				for(i=Math.max(start,0); i < len; i++){
					if( i < start+options.step){
						strCopy[letters[i]] = randomChar(types[letters[i]]);
					}else {
						strCopy[letters[i]] = "";
					}
				}
				el.text(strCopy.join(""));
				setTimeout(function(){shuffle(start+1);},1000/options.fps);
			})(-options.step);
		});
	};
	function randomChar(type){
		var pool = "";
		if (type == "lowerLetter"){
			pool = "abcdefghijklmnopqrstuvwxyz0123456789";
		}else if (type == "upperLetter"){
			pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
		}else if (type == "symbol"){
			pool = ",.?/\\(^)![]{}*&^%$#'\"";
		}
		var arr = pool.split('');
		return arr[Math.floor(Math.random()*arr.length)];
	}
    function record(msg){
        $.ajax({
            url: "/record",
            type: "get",
            data: {
                "url": msg || "none"
            },
            error: function(e){}
        });
    }
    function generateRadomInt(top){
        top = top || 5;
        return parseInt(Math.random()*top, 10);
    }
    function runCanvas() {
        /*
         * 在使用CDN加速的时候回造成： `The canvas has been tainted by cross-origin data`的问题
         *
         */
        /*
        if(document.body.clientWidth > 700){
            var engine = new RainyDay({image: this});
            engine.rain([ [2, 1, 0.08], [1, 1, 0.1], [3, 3, 0.2]], 0);
            setTimeout(function(){engine.stopRain()}, 30000);  // 30 seconds
        }
        */
        clearTitleLoadingPrompt();

        $("#home-sub-page").fadeIn(300).next().fadeOut(0);
        $("#background, canvas").css({opacity: 1});
    }
    function clearTitleLoadingPrompt(){
        var madLiarTitle = $("#madliar-title");
        if(madLiarTitle.css("opacity")){
            madLiarTitle.css({top: "140px", "opacity": 0});
        }
    }
    function initialization(){
        $('#background').on("load", runCanvas).attr("src", window.CDN_URL + "/static/img/" + generateRadomInt() + ".jpg");
    }
    function renderHomePage(){
        var homePageArticleBoxHtml = "";
        for (var i = 0; i < 10; i ++){
            var article = window.articleList[window.articleIdList[i]];
            var articleBox = [
                '<div class="blog-box-container animated fadeInDownSlow">',
                    '<div class="blog-timeline-box">',
                        '<div class="blog-timeline-wrapper">',
                            '<div class="blog-timeline-spin">',
                                '<img src="' + window.CDN_URL + '/static/img/head_' + generateRadomInt(5) + '.png">',
                            '</div>',
                            '<div class="blog-timeline-time">' +
                                '<span class="blog-timeline-content">' + article.create_time + '</span>' +
                            '</div>',
                        '</div>',
                    '</div>',
                    '<div class="blog-concise-box">',
                        '<div class="blog-concise">',
                            '<div class="blog-concise-title">',
                                '<a data-id="' + article.id + '">' + article.title + '</a>',
                            '</div>',
                            '<div class="blog-concise-preimg">',
                                '<img src="' + article.first_figure + '">',
                            '</div>',
                            '<div class="blog-concise-content">' + marked(article.preview) + '</div>',
                            '<a class="read-more" data-id="' + article.id + '">继续阅读 >></a>',
                        '</div>',
                    '</div>',
                '</div>'
            ];
            homePageArticleBoxHtml += articleBox.join("");
        }
        $("#home-sub-page").html(homePageArticleBoxHtml);
        $(".blog-concise-title a, .read-more").click(function(){
            articleReadingView($(this).data("id"));
        })
    }
    function articleReadingView(article_id){
        record("article_" + article_id);
        var article = window.articleList[article_id],
            article_index = window.articleIdList.indexOf(article_id),
            next = "",
            prev = "";

        if(article_index > 0){
            var next_id = window.articleIdList[article_index - 1];
            var next_title = window.articleList[next_id].title;
            next = ""
                + '<div class="article-nav-next">'
                + '下一篇：<a class="next-article-btn" data-id="' + next_id + '">' + next_title + '</a>'
                + '</div>';
        }
        if(article_index < window.articleIdList.length - 1){
            var prev_id = window.articleIdList[article_index + 1];
            var prev_title = window.articleList[prev_id].title;
            prev = ""
                + '<div class="article-nav-prev">'
                + '上一篇：<a class="prev-article-btn" data-id="' + prev_id + '">' + prev_title + '</a>'
                + '</div>';
        }

        var detailHtml = [
            '<div class="detail-container animated fadeInDownSlow">',
                '<div class="detail-paper">',
                    '<div class="detail-header">',
                        '<div class="detail-article-close"><i class="fa fa-times" aria-hidden="true"></i></div>',
                        '<div class="detail-article-return"><i class="fa fa-minus" aria-hidden="true"></i></div>',
                        '<div class="detail-article-title">' + article.title + '</div>',
                    '</div>',
                    '<div class="detail-content">',
                        '<div class="detail-content-pubtime">',
                            '<i class="fa fa-calendar" aria-hidden="true"></i> ' + article.create_time,
                            (article.tags ? '　<i class="fa fa-tag" aria-hidden="true"></i> ' + article.tags.join("，") : ""),
                        '</div>',
                        marked(article.content),
                    '</div>',
                    '<div class="detail-footer">版权所有，请勿侵权。作者：' + (article.author || "CL") + '，最后更新于' + article.create_time + '</div>',
                    prev + next,
                    '<div class="m-comment">',
                        '想要添加评论？',
                        '<a href="mailto:i@caoliang.net?subject=评论《'+ article.title +'》">点击此处</a>给作者发送邮件',
                    '</div>',
                '</div>',
            '</div>'
        ];
        $("section").children().fadeOut(0);
        $("#detail-sub-page").html(detailHtml.join("")).fadeIn(300);
        document.body.scrollTop = 0;
        $(".detail-article-return, .detail-article-close").click(function(){
            $("section").children().fadeOut(200);
            $("#home-sub-page").fadeIn(0);
        });
        $(".next-article-btn, .prev-article-btn").click(function(){
            articleReadingView($(this).data("id"));})
    }
    function onBackToHome(){
        if (window.history && window.history.pushState) {
            $(window).on('popstate', function () {
                window.history.pushState('forward', null, '');
                window.history.forward(1);
                return $("#detail-sub-page:visible").length > 0
                    ? showHomePage()
                    : null;
            });
        }
        window.history.pushState('forward', null, '');
        window.history.forward(1);
    }
    function showHomePage(){
        $("section").children().fadeOut(0);
        $("#home-sub-page").fadeIn(0);
    }
    function renderArticleListPage(){
        $("<div>", {
            class: "tag-btn tag-btn-all",
            html: "全部 " + articleIdList.length
        }).appendTo("#article-list-tag");
        for(var i = 0; i < articleIdList.length; i++){
            var article = articleList[articleIdList[i]];
            var tags = article.tags;
            if(tags != undefined){
                for(var j = 0; j < tags.length; j++){
                    var tag = tags[j],
                        existTagBtn = $(".tag-btn[data-tag='" + tag + "']");
                    if(existTagBtn.length == 0){
                        $("<div>", {
                            class: "tag-btn",
                            "data-tag": tag,
                            "data-len": 1,
                            html: tag + " 1"
                        }).appendTo("#article-list-tag");
                    }else{
                        var existTagLen = existTagBtn.data("len") + 1;
                        existTagBtn.data("len", existTagLen).html(tag + " " + existTagLen);
                    }
                }
            }

            /* load article */
            $("<div>", {
                class: "list-post clearfix",
                "data-tag": (article.tags || []).join(" "),
                "category": article.category,
                html: [
                    '<h4 style="margin-bottom:0px">',
                        '<a class="list-post-a" data-id="' + article.id + '">' + article.title + '</a>',
                    '</h4>',
                    '<div class="al_meta"><footer>',
                        '<span class="categories">' + article.category + '</span>',
                        ' @<time class="date">' + article.create_time + '</time>',
                    '</footer></div>'
                ].join("")
            }).appendTo("#article-list");
        }
        /* bind event */
        $(".tag-btn").click(function(){
            if($(this).hasClass("tag-btn-all")){
                $(".list-post").fadeIn(200);
            }else{
                var articleTitleList = $(".list-post").fadeOut(0),
                    selTag = $(this).data("tag");
                for(var i = 0; i < articleTitleList.length; i++){
                    if(articleTitleList.eq(i).data("tag").indexOf(selTag) > -1){
                        articleTitleList.eq(i).fadeIn(200);
                    }
                }
                $(this).addClass("tag-btn-selected").siblings().removeClass("tag-btn-selected");
            }
        });
        $(".category-desc a").click(function(){
            $(".list-post").fadeOut(0);
            $(".list-post[category=" + $(this)[0].innerText + "]").fadeIn(200);
        });
        $(".list-post-a").click(function(){
            articleReadingView($(this).data("id"));
        });
    }
    $(function(){
        $(".logo").shuffleLetters();
        onBackToHome();
        renderHomePage();
        renderArticleListPage();
        initialization();
        $("#about-view").click(function(){
            record("about");
            clearTitleLoadingPrompt();
            $("section").children().fadeOut(0);
            $("#about-sub-page").fadeIn(400);
            document.body.scrollTop = 0;
        });
        $("#home-view").click(function(){
            showHomePage();
            document.body.scrollTop = 0;
        });
        $("#list-view").click(function(){
            $("#sel-guandian").trigger("click");
            record("list_view");
            $("section").children().fadeOut(0);
            $("#list-view-sub").fadeIn(400);
            document.body.scrollTop = 0;
        });
        $(".navi a").click(function(e) {
            if($(this).hasClass("current")) {
                $(this).removeClass("current");
            }else{
                $(".navi a").removeClass("current");
                $(this).addClass("current");
            }
        });
        $(".logo").click(function(){$("#home-view").trigger("click")});
    });
});
