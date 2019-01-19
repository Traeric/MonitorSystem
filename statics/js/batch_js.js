// 具体的业务实现
function sendMsg(layero, layer, index, batchType) {
    // 获取到选中的主机
    let checkDoms = $(".host-to-remote-user:checked");
    // 主机去重
    let host_to_remote_user_ids = [];
    $.each(checkDoms, function (index, item) {
        if (host_to_remote_user_ids.indexOf($(item).val()) === -1) {
            host_to_remote_user_ids.push($(item).val());
        }
    });
    // 判断主机不能为空
    if (!host_to_remote_user_ids.length) {
        // 文字提示框的文字变成红色
        $(layero).children('#LAY_layuipro').children().eq(0).children("b").css("color", "#f00");
        $(layero).children('#LAY_layuipro').children().eq(0).children("b").html("必须选择主机！");
        return;
    }
    // 要发送的数据
    let sendData = {"host-to-remote-user-ids": host_to_remote_user_ids};
    if (batchType === 'cmd') {              // 命令操作
        // 获取要执行的命令
        let command = $(".cmd").eq(0).val().trim();
        if (!command) {
            $(layero).children('#LAY_layuipro').children().eq(0).children("b").css("color", "#f00");
            $(layero).children('#LAY_layuipro').children().eq(0).children("b").html("批量命令不能为空！");
            return;
        }
        sendData['command'] = command;
        sendData['batch-type'] = batchType;
    } else if (batchType === "file_transfer") {     // 文件传输
        sendData['batch-type'] = batchType;
        // 获取文件传输类型
        let transfer_type = $("#file_transfer_hook option:selected").val().trim();
        if (transfer_type === "file_upload") {          // 远程上传
            // 获取文件在堡垒机上的位置
            let file_path = window.localStorage.getItem("file_path");
            if (!file_path) {
                // 没有选择上传的文件
                $(layero).children('#LAY_layuipro').children().eq(0).children("b").css("color", "#f00");
                $(layero).children('#LAY_layuipro').children().eq(0).children("b").html("请选择要发送到远程主机的文件！");
                return
            }
            // 获取要传送到远程的路径
            let remote_path = $("#remote_path_hook").val().trim();
            if (!remote_path) {
                $(layero).children('#LAY_layuipro').children().eq(0).children("b").css("color", "#f00");
                $(layero).children('#LAY_layuipro').children().eq(0).children("b").html("请选择要发送到远程主机的位置！");
                return;
            }
            // 删除localStorage的上传文件的路径
            window.localStorage.removeItem("file_path");
            // 整理发送的数据
            sendData['batch-type'] = transfer_type;   // 批量命令执行的类型
            sendData['file_path'] = file_path;      // 上传文件在堡垒机的位置
            sendData['remote_path'] = remote_path;   // 传送到远程主机的位置
            // 恢复文件提示
            let fileInfoDom = $("#file_info_hook");
            fileInfoDom.html("选择要传送的文件，点击上传，或将文件拖拽到此处");
            fileInfoDom.css({
                color: "#999",
                fontWeight: "normal",
            });
        } else if (transfer_type === "file_download") {         // 远程下载
            // 获取远程路径
            let remotePathObj = {};
            $(".remote-host_id").each((index, item) => {
                // 获取主机的id
                let hostId = $(item).data("hostid");
                // 获取远程路径
                let remotePath = $(item).val().trim();
                if (remotePath) {
                    remotePathObj[hostId] = remotePath;
                }
            });
            if ($.isEmptyObject(remotePathObj)) {
                $(layero).children('#LAY_layuipro').children().eq(0).children("b").css("color", "#f00");
                $(layero).children('#LAY_layuipro').children().eq(0).children("b").html("远程路径不能为空！");
                return;
            }

            // 整理发送的数据
            sendData['batch-type'] = transfer_type;   // 批量命令执行的类型
            sendData['remote_path'] = JSON.stringify(remotePathObj);   // 从远程主机下载文件的路径
        }
    }
    // 发送
    $.ajax({
        url: "/monitor/batch_cmd/",
        type: "post",
        traditional: true,
        headers: {'X-CSRFToken': csrfToken},
        data: sendData,
        dataType: 'JSON',
        success(args) {
            // 将task_id存起来
            window.taskId = args[0]["id"];
            let statusChoices = args[args.length - 1];
            window.coloeSelector = ["info", "success", "danger", "warning"];
            args.pop();
            /**
             * 将任务栏的信息更新
             */
            {
                $(".target-id:eq(0)").html("任务ID：" + args[0]['id']);
                $(".target:eq(0)").html("总任务" + args.length);
                $(".finished:eq(0)").html("已完成0");
                $(".defeat:eq(0)").html("失败0");
                $(".rest:eq(0)").html("剩余" + args.length);
                window.finished = 0;
                window.rest = args.length;
                window.defeat = 0;
            }
            // 清除之前的内容
            $(".information-area:eq(0)").empty();
            $.each(args, function (index, item) {
                let infoStr = `
                            <div class="item">
                                <div class="head">
                                    <i class="fa fa-plus-square-o" onclick="iToggle(this);"></i>
                                    <span class="label label-primary">${item['tasklogdetail__host_to_remote_users__host__name']}(${item['tasklogdetail__host_to_remote_users__host__ip_addr']})</span>
                                    <span class="label label-warning">User: ${item['tasklogdetail__host_to_remote_users__remote_user__username']}</span>
                                    <span class="label label-info">System: ${item['tasklogdetail__host_to_remote_users__host__os_type']}</span>
                                    <span class="label label-${coloeSelector[item['tasklogdetail__status']]}">Result: ${statusChoices[item['tasklogdetail__status']]}</span>
                                </div>
                                <div class="show">
                                    <div class="alert alert-${coloeSelector[item['tasklogdetail__status']]}">
                                        <b>${item['tasklogdetail__host_to_remote_users__host__name']}-${item['tasklogdetail__host_to_remote_users__host__os_type']}!</b>
                                        <br>
                                        <pre id="${item['tasklogdetail__host_to_remote_users__host__name']}_${item['tasklogdetail__host_to_remote_users__remote_user__username']}"
                                             style="background: none; border: none;">
                                            waiting for get data...<i class="layui-icon layui-icon-loading layui-icon layui-anim layui-anim-rotate layui-anim-loop"></i>
                                        </pre>
                                    </div>
                                </div>
                            </div>
                        `;
                // 添加到information-area中
                $(".information-area:eq(0)").append(infoStr);
            });
            // 禁用执行命令的按钮
            let btn = $(".execute-btn:eq(0)");
            btn.attr("disabled", "disabled");
            btn.css({
                "cursor": "not-allowed",
            });
            // 关闭弹窗
            layer.close(index);
            // 启动websocket实时拿到更新的主机信息
            webSocket();
        },
    });
}

layui.use('layer', function () {
    let $ = layui.jquery, layer = layui.layer;
    //触发事件
    let active = {
        notice: function () {
            layer.open({
                type: 1
                , title: false
                , closeBtn: 2
                , area: '600px;'
                , anim: 4
                , resize: false
                , id: 'LAY_layuipro' //设定一个id，防止重复弹出
                , btn: ['确认', '取消']
                , moveType: 1 //拖拽模式，0或者1
                , content: `<div style="padding: 50px; line-height: 22px; background-color: #393D49;
                                        color: #FFB800; font-weight: 300; text-align: center;">
                                       <b>确定要批量执行该命令吗？</b>
                                   </div>`
                , yes: function (index, layero) {
                    // 获取文件发送的类型
                    let batchType = $('.execute-btn:eq(0)').data('batch').trim();
                    // 确认后发送信息
                    sendMsg(layero, layer, index, batchType);
                }
            });
        },
    };
    $('.layui-btn').on('click', function () {
        let othis = $(this), method = othis.data('method');
        active[method] ? active[method].call(this, othis) : '';
    });
});


/**
 * 启动websocket
 */
function webSocket() {
    if (window.s) {
        window.s.close()
    }
    let socket = new WebSocket("ws://" + window.location.host + "/monitor/host_detail_info/");
    socket.onopen = function () {
        // 将task_id发送过去
        socket.send(window.taskId);
    };
    socket.onmessage = function (e) {
        let data_arr = JSON.parse(e.data);
        // 将任务栏的状态更新
        window.rest--;
        window.finished++;
        $(".finished:eq(0)").html("已完成" + window.finished);
        $(".rest:eq(0)").html("剩余" + window.rest);
        if (data_arr[3] * 1 === 2 || data_arr[3] * 1 === 3) {
            window.defeat++;
            $(".defeat:eq(0)").html("失败" + window.defeat);
        }
        // 将消息推送显示
        let dom = $(`#${data_arr[0]}_${data_arr[1]}`);
        // 改变提示框样式
        dom.parent().removeClass("alert-info").addClass("alert-" + window.coloeSelector[data_arr[3]]);
        let domChildren = dom.parent().parent().prev().children();
        $(domChildren[domChildren.length - 1]).removeClass("label-info").addClass("label-" + window.coloeSelector[data_arr[3]]);
        let result = ["initialized", "success", "failed", "timeout"];
        $(domChildren[domChildren.length - 1]).html("Result: " + result[data_arr[3]]);
        // 将结果返回到显示区域
        dom.html(data_arr[2]);
    };
    socket.onclose = function () {
        // 关闭后将发送命令按钮恢复
        let btn = $(".execute-btn:eq(0)");
        btn.removeAttr("disabled");
        btn.css({
            "cursor": "pointer",
        });
    };
    window.s = socket;
}
