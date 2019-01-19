/**
 * 主机选择事件，只在远程下载文件的时候触发
 */
let flag = true;     // 是否绑定点击事件
function hostSelect() {
    // 获取主机信息
    let hostInfo = $(this).children("span:eq(0)").html();
    let hostId = $(this).prev().val();
    // 查看有没有重复
    if (distinct(hostId, this.isSelect)) {
        this.isSelect = !this.isSelect;
        return;
    }
    if (this.isSelect) {
        // 添加input框到右侧面板
        let str = `
            <div id="${hostId}" class="layui-form layui-form-pane" style="margin-top: 10px;">
                <div class="layui-form-item">
                    <label class="layui-form-label">远程路径</label>
                    <div class="layui-input-inline" style="margin-top: 0; min-width: 300px;">
                        <input placeholder="${hostInfo}" autocomplete="off" class="layui-input remote-host_id"
                               type="text" data-hostid="${hostId}">
                    </div>
                </div>
            </div>
        `;
        $(".file_download-area:eq(0)").append(str);
    } else {
        // 移除输入框
        $(`#${hostId}`).remove();
    }
    this.isSelect = !this.isSelect;
}

function distinct(addId, isSelect) {
    // 获取所有的已经添加的id
    let idList = $(".remote-host_id");
    let distincted = false;
    idList.each((index, item) => {
        let id = $(item).data("hostid");
        if ((parseInt(id) === parseInt(addId)) && isSelect) {
            distincted = true;
        }
    });
    return distincted;
}

/**
 * let all checked host display on left panel as input style
 */
function initHostInput(host_to_remote_users) {
    if (host_to_remote_users.length > 0) {
        // 清空右侧的面板
        $("#remote_host_showing").empty();
    }

    // 循环添加到右侧面板
    $.each(host_to_remote_users, (index, item) => {
        // 获取主机信息
        let hostId = $(item).val();
        let hostInfo = $(item).next().children("span:eq(0)").html();
        // 添加到右侧面板
        let str = `
            <div id="${hostId}" class="layui-form layui-form-pane" style="margin-top: 10px;">
                <div class="layui-form-item">
                    <label class="layui-form-label">远程路径</label>
                    <div class="layui-input-inline" style="margin-top: 0; min-width: 300px;">
                        <input placeholder="${hostInfo}" autocomplete="off" class="layui-input remote-host_id"
                               type="text" data-hostid="${hostId}">
                    </div>
                </div>
            </div>
        `;
        $("#remote_host_showing").append(str);
    });
}

