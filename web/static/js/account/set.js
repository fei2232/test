/**
 * Created by Administrator on 2018-09-12.
 */
;
var account_set_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $(".wrap_account_set .save").click(function () {

            var btn_traget = $(this);
            if(btn_traget.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交")
                return;
            }
            //参数获取部分
            // 用户名
            var user_name_target = $(".wrap_account_set input[name = user_name]");
            var user_name = user_name_target.val();
            // 用户密码
            var user_pwd_target = $(".wrap_account_set input[name = user_pwd]");
            var user_pwd = user_pwd_target.val();
            // 用户状态
            var user_status_target = $(".wrap_account_set select[name = user_status]");
            var user_status = user_status_target.val();
            // 备注信息
            var user_remark_target = $(".wrap_account_set input[name = user_remark]");
            var user_remark = user_remark_target.val();


            // 参数校验部分
            if( user_name.length < 1)
            {
                common_ops.tip("请输入符合规范的用户名！",user_name_target);
                return false;
            }
            if(user_pwd.length < 6)
            {
                common_ops.tip("请输入符合规范的用户密码！",user_pwd_target);
                return false;
            }
            if(user_status.length < 1)
            {
                common_ops.tip("请输入符合规范的用户状态！",user_status_target);
                return false;
            }
            if(user_remark.length < 1)
            {
                common_ops.tip("请输入符合规范的备注信息！",user_remark_target);
                return false;
            }

            btn_traget.addClass("disabled");

            var data = {
                user_name:user_name,
                user_pwd:user_pwd,
                user_status:user_status,
                user_remark:user_remark,
                user_id:$(".wrap_account_set input[name = user_id]").val(),
            };

            $.ajax({
                url:common_ops.buildUrl("/account/set"),
                type:"POST",
                data:data,
                dataType:"json",
                success:function (res) {
                    btn_traget.removeClass("disabled");
                    var callback = null;
                    if(res.code == 200){
                        callback = function () {
                            window.location.href =common_ops.buildUrl("/account/index");
                        }
                    }
                    common_ops.alert(res.msg,callback);
                }
            });



        });
    }
}

$(document).ready( function () {
        account_set_ops.init();
    }
);