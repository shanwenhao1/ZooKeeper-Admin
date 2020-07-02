/*global json show*/

function mFirm(btnId) {
    var jsonBtn = document.getElementById(btnId);
    if(confirm("确定修改")){
        // 解析json(附有检查格式的功能)
        var jsonData = JSON.parse(jsonBtn.innerText);
        var postJson = {};
        postJson["nodeId"] = btnId;
        postJson["nodeData"] = jsonData;
        postJson["action"] = "Modify";
        var postData = JSON.stringify(postJson, null, 2);
        $.ajax({
            type: "POST",
            url: "",
            contentType: "application/json; charset=utf-8",
            data: postData,
            dataType: "json",
            success: function (data) {
                data = JSON.parse(JSON.stringify(data));
                if (data["status"] === 0){
                    alert("修改成功");
                    location.reload();
                }else{
                    alert("修改失败: " + data["errMsg"])
                }
             },
            error: function () {
                data = JSON.parse(JSON.stringify(data))
                alert("修改失败, 提交未成功" + data["errMsg"]);
            }
        });
    }else{
        // alert("取消");
    }
}

function dFirm(btnId) {
    var jsonBtn = document.getElementById(btnId);
    if(confirm("确定删除")){
        // 解析json(附有检查格式的功能)
        var postJson = {};
        postJson["nodeId"] = btnId;
        postJson["action"] = "Delete";
        var postData = JSON.stringify(postJson, null, 2);
        $.ajax({
            type: "POST",
            url: "",
            contentType: "application/json; charset=utf-8",
            data: postData,
            dataType: "json",
            success: function (data) {
                data = JSON.parse(JSON.stringify(data));
                if (data["status"] === 0){
                    alert("删除成功");
                    location.reload();
                }else{
                    alert("删除失败: " + data["errMsg"])
                }
             },
            error: function (data) {
                data = JSON.parse(JSON.stringify(data))
                alert("删除失败: " + data["errMsg"]);
            }
        });
    }
}


function syntaxHighlight(json) {
    if (typeof json != 'string') {
        json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function(match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

function jsonDisplay(json, btnId) {
    var options = {
        mode: 'tree',
        modes: ['code', 'form', 'text', 'tree', 'view'], // allowed modes
        onError: function (err) {
          alert(err.toString());
        },
        onModeChange: function (newMode, oldMode) {
          console.log('Mode switched from', oldMode, 'to', newMode);
        }
      };
    var btn = document.getElementById(btnId + 'B');
    var pre = document.getElementById(btnId);
    var mBtn = document.getElementById(btnId + 'M');
    var dBtn = document.getElementById(btnId + 'D');

    // 调用jsonEditor保存json数据
    // var editorJson = JSON.parse(JSON.stringify(json, null, 2));
    var editor = new JSONEditor(pre, options, json);
    // editor.set(editorJson);
    if (btn.value === "+"){
        btn.value = "-";
        // contenteditable='true'表明pre是可编辑的
        pre.innerHTML = "<td colspan='4'><pre contenteditable='true'><code>" + syntaxHighlight(editor.get()) + "</code></pre></td>";
        // 监听tab键的js function
        pre.addEventListener("keydown", function(e){
            if(e.keyCode === 9){
                document.execCommand('insertText', false, '  ');
                // 阻止浏览器执行与事件关联的默认动作(此处为阻止tab)
                e.preventDefault();
            }
        });
        // pre.innerHTML = "<td colspan='4'><pre contenteditable='true'><code>" + syntaxHighlight(json) + "</code></pre>";
        mBtn.innerHTML = "<input type='button' style='background: #ffff00; color: #faaccc' value='modify'/>";
        // mBtn.onclick = mFirm; onclick无参数可直接调用, 有参数则需要使用function
        mBtn.onclick = function(){ mFirm(btnId) };
        dBtn.innerHTML = "<input type='button' style='background: #ffff00; color: #faaccc' value='delete'/>";
        dBtn.onclick = function () { dFirm(btnId) };
    }else{
        btn.value = "+";
        pre.innerHTML = '';
        mBtn.innerHTML = '';
        dBtn.innerHTML = '';
    }
    editor.destroy();
}

function docJsonDisplay(json, id) {
    var options = {
        mode: 'tree',
        modes: ['code', 'form', 'text', 'tree', 'view'], // allowed modes
        onError: function (err) {
          alert(err.toString());
        },
        onModeChange: function (newMode, oldMode) {
          console.log('Mode switched from', oldMode, 'to', newMode);
        }
    };
    var pre = document.getElementById(id);
    // 调用jsonEditor保存json数据
    // var editorJson = JSON.parse(JSON.stringify(json, null, 2));
    var editor = new JSONEditor(pre, options, json);
    var newHtml = syntaxHighlight(editor.get());
    pre.innerHTML = "<td colspan='4'><pre contenteditable='false'><code>" + newHtml + "</code></pre></td>";
    editor.destroy();
}