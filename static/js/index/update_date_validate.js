/**
 * created by DELL on 2020/5/19
 */
$(function () {
    let $button_submit = $('input#add'); //提交按钮
    let $date_f = $('input[name="date_f"]'); // 年月
    let $date = $('input[name="date"]'); // 日期
    let $name = $('input[name="name"]'); // 用途
    let $payment = $('input[name="payment"]'); // 金额
    // let $type = $('input[name="type"]'); // 类型
    let $note = $('textarea[name="note"]'); // 备注

    var web_url = window.location.host;
    let url = 'http://' + web_url + '/add';
    // 日期验证
    $date.blur(function () {
        fn_check_date();
    });
    // 用途校验
    $name.blur(function () {
        fn_check_name();
    });
    // 金额校验
    $payment.blur(function () {
        fn_check_payment();
    });

    $button_submit.click(function (e) {
        // 阻止默认提交操作
        e.preventDefault();
        if (fn_check_date() !== 'success'){
            return
        }
        if (fn_check_name() !== 'success'){
            return
        }
        if  (fn_check_payment() !== 'success'){
            return
        }
        var type = $('input[name="type"]:checked').val();
        let data = {
            'date': $date.val(),
            'date_f': $date_f.val(),
            'name': $name.val(),
            'payment': $payment.val(),
            'type': type,
            'note': $note.val(),
        };
        $.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify(data),
            // 请求内容的数据类型（前端发给后端的格式）
            contentType: "application/json; charset=utf-8",
            async: false,	// 关掉异步功能
        })
        .done(function (res) {
            if (res.code === 0){
                message.showSuccess(res.message);
                setTimeout(function () {
                location.reload();
              }, 1000);
            }else {
              // 注册失败，打印错误信息
              message.showError(res.message);
            }
        })
        .fail(function(){
            message.showError('服务器超时，请重试！');
        });

    });


    function fn_check_date() {
        var date = $date.val();
        if (date === ''){
            message.showError('日期不能为空！');
            return
        }
        if (!(/^\d_\d{1,2}$/).test(date)){
            message.showError('日期格式不正确！');
            return
        } else {
            return 'success';
        }
    }
    function fn_check_name() {
        var name = $name.val();
        if (name === ''){
            message.showError('用途不能为空！');
        } else {
            return 'success';
        }
    }
    function fn_check_payment() {
        var payment = $payment.val();
        if (payment === ''){
            message.showError('金额不能为空！');
            return
        }
        if (!(/^[1-9]\d*\.\d*|0\.\d*[1-9]\d*|\d+$/).test(payment)){
            message.showError('金额格式不正确');
            return
        } else {
            return 'success';
        }
    }

});
