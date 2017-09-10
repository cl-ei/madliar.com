$.cl = {
    fileIcon: "/static/img/jstree/file.png",
    folderIcon: "/static/img/jstree/folder.png",
    setCookie: function (key, value, expiredays){
        var exdate=new Date();
        exdate.setDate(exdate.getDate() + expiredays);
        document.cookie = key + "=" + encodeURI(value)
            + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString())
    },
    getCookie: function (key) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                 var cookie = jQuery.trim(cookies[i]);
                 if (cookie.substring(0, key.length + 1) == (key + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(key.length + 1));
                     break;
                 }
             }
        }
        return cookieValue;
    },
    windowSizeMonitor: function (){
        if(document.documentElement.clientWidth < 605){
            $("#nav, #content").css({"display": "none"});
            $("#uavaliable-mask").css({"display": "block"});
        }else{
            $("#nav, #content").css({"display": "block"});
            $("#uavaliable-mask").css({"display": "none"});
        }
    },
    popupMessage: function (msg, title){
        var promptModal = $(".cl-prompt");
        if(promptModal.css("opacity") > 0){
            $.cl.clearMessage();
            setTimeout(function(){
                $.cl.popupMessage(msg, title)
            }, 200);
        }else{
            $("#cl-prompt-title").html(title || "提示");
            $("#cl-prompt-content").html(msg);
            promptModal.css({"opacity": "1", "top": "20px", "z-index": "10"}).children().eq(0).off("click").click($.cl.clearMessage);
        }
    },
    clearMessage: function (){
        $(".cl-prompt").css({"opacity": "0", "top": "0px", "z-index": "-10"});
    },
    onLoginOrRegisted: function (data){
        if(data.err_code != 0){
            var msg = "操作失败。详细信息：" + data.err_msg;
            $.cl.popupMessage(msg);
            return ;
        }
        $.cl.setCookie("madToken", data.token);
        $.cl.setCookie("email", data.email);
        window.contextData.loginInfo = {
            email: data.email
        };
        $.cl.renderLoginPage();
    },
    login: function (){
        var email = $("input[name=email]").val(),
            password = $("input[name=password]").val();
        if(email.length < 1 || password.length > 32 || password.length < 5){
            $.cl.popupMessage("请输入正确的邮箱和密码。");
            return ;
        }
        $.ajax({
            url: "/notebook/api",
            type: "post",
            data: {
                action: "login",
                email: email,
                password: password
            },
            success: $.cl.onLoginOrRegisted,
            error: function(e){
                $.cl.popupMessage("操作失败，请检查你的网络连接。");
            }
        })
    },
    logout: function (){
        $.ajax({
            url: "/notebook/api",
            type: "post",
            data: {
                action: "logout"
            },
            success: function(data){
                if(data.err_code != 0){
                    var msg = "操作失败。详细信息：" + data.err_msg;
                    $.cl.popupMessage(msg);
                    return ;
                }
                window.contextData.loginInfo = false;
                $.cl.renderUnloginPage();
            },
            error: function(e){
                $.cl.popupMessage("操作失败，请检查你的网络连接。");
            }
        })
    },
    regist: function (){
        var email = $("input[name=email]").val(),
            password = $("input[name=password]").val();
        if(email.length < 1 || password.length > 32 || password.length < 5){
            $.cl.popupMessage("请输入正确的邮箱和密码。");
            return ;
        }
        $.ajax({
            url: "/notebook/api",
            type: "post",
            data: {
                action: "regist",
                email: email,
                password: password
            },
            success: $.cl.onLoginOrRegisted,
            error: function(e){
                $.cl.popupMessage("操作失败，请检查你的网络连接。");
            }
        })
    },
    getAndRenderDefaultFileListAndPage: function(){
        var jstreeInstance = $("#jstree");
        if (jstreeInstance.jstree()){
            jstreeInstance.jstree().destroy()
        }
        jstreeInstance.jstree({
            core: {
                data: [{
                    text: "游客的文件夹",
                    state: {opened: true},
                    children: [{
                        text: "简介",
                        type: "file",
                        state: {opened: true, selected: true}
                    }]
                }]
            },
            types: {
                file: {icon: $.cl.fileIcon},
                foler: {icon: $.cl.folderIcon},
                default: {icon: $.cl.folderIcon}
            },
            plugins: ["types"]
        });
        document.getElementById('input-text-area').value = $("#default-file-content").val();
    },
    getAndRenderLoginedFileListAndPage: function(){
        var jstreeInstance = $("#jstree");
        if (jstreeInstance.jstree()){
            jstreeInstance.jstree().destroy()
        }
        jstreeInstance.jstree({
            core: {
                data: {
                    url: "/notebook/api",
                    type: "post",
                    data: function (node) {
                        return {
                            id: node.id,
                            action: "get_file_list"
                        };
                    }
                }
            },
            types: {
                file: {icon: $.cl.fileIcon},
                foler: {icon: $.cl.folderIcon},
                default: {icon: $.cl.folderIcon}
            },
            plugins: ["types"]
        });
        document.getElementById('input-text-area').value = "";
    },
    renderLoginPage: function (){
        $.cl.releasePageResource();
        var navHtml = [
            '<span class="user-name">欢迎回来，' + window.contextData.loginInfo.email + '</span>',
            '<a href="javascript:void(0)" id="logout" ><i class="fa fa-sign-in" aria-hidden="true"></i> 注销</a>'
        ].join("");
        $(".right-nav").html(navHtml);
        $("#logout").off("click").click($.cl.logout);

        var leftNavHtml = [
            '<a href="javascript:void(0)" id="save-btn"><i class="fa fa-save" aria-hidden="true"></i> 保存</a>'
        ].join("");
        $("#top-dynamic-nav").html(leftNavHtml);
        $.cl.getAndRenderLoginedFileListAndPage()
    },
    releasePageResource: function (){

    },
    renderUnloginPage: function (){
        $.cl.releasePageResource();
        var navHtml = [
            '<a href="javascript:void(0)" id="login" ><i class="fa fa-sign-in" aria-hidden="true"></i> 登录</a>',
            '<a href="javascript:void(0)" id="register" ><i class="fa fa-table" aria-hidden="true"></i> 注册</a>'
        ].join("");
        $(".right-nav").html(navHtml);
        $("#login").off("click").click(function(){
            $("#login-or-regist").html("登录");
            $("#login-modal").modal("show");
        }).next().off("click").click(function(){
            $("#login-or-regist").html("注册");
            $("#login-modal").modal("show");
        });
        $("#login-btn").off("click").click(function(){
            $("#login-modal").modal("hide");
            return $("#login-or-regist").html() === "注册" ? $.cl.regist() : $.cl.login();
        });
        $.cl.getAndRenderDefaultFileListAndPage();
    },
    daemonToTransMdId: undefined,
    oldContent: undefined,
    daemonToTransMd: function (){
        return setInterval(function(){
            var newContent = $("#input-text-area").val();
            if (newContent !== $.cl.oldContent){
                $.cl.oldContent = newContent;
                $("#content-text").html(marked(newContent));
            }
        }, 400);
    },
    initPage: function (){
        (window.contextData.loginInfo && window.contextData.loginInfo.email ? $.cl.renderLoginPage : $.cl.renderUnloginPage)();
        $("input[name=password]").on('keyup', function(e){if(e.key === "Enter"){$("#login-btn").trigger("click")}});
        if ($.cl.daemonToTransMdId){
            clearInterval($.cl.daemonToTransMdId);
        }
        $.cl.daemonToTransMdId = $.cl.daemonToTransMd();
    }
};
$(window).resize($.cl.windowSizeMonitor).on("ready", $.cl.windowSizeMonitor);$($.cl.initPage);