/**
 * Created by Administrator on 2018-09-12.
 */
;
var oil_set_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $(".wrap_oil_set .save").click(function () {

            var btn_traget = $(this);
            if(btn_traget.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交")
                return;
            }
            //参数获取部分
            // 油品名
            var oil_name_target = $(".wrap_oil_set input[name = oil_name]");
            var oil_name = oil_name_target.val();
            // 油品密度
            var oil_density_target = $(".wrap_oil_set input[name = oil_density]");
            var oil_density = oil_density_target.val();
            // 油品状态
            var oil_status_target = $(".wrap_oil_set select[name = oil_status]");
            var oil_status = oil_status_target.val();
            // 备注信息
            var oil_remark_target = $(".wrap_oil_set input[name = oil_remark]");
            var oil_remark = oil_remark_target.val();


            // 参数校验部分
            if( oil_name.length < 1)
            {
                common_ops.tip("请输入符合规范的油品名称！",oil_name_target);
                return false;
            }
            if(oil_density.length < 1)
            {
                common_ops.tip("请输入符合规范的油品密度！",oil_density_target);
                return false;
            }
            if(oil_status.length < 1)
            {
                common_ops.tip("请输入符合规范的油品状态！",oil_status_target);
                return false;
            }
            if(oil_remark.length < 1)
            {
                common_ops.tip("请输入符合规范的备注信息！",oil_remark_target);
                return false;
            }

            btn_traget.addClass("disabled");

            var data = {
                oil_name:oil_name,
                oil_density:oil_density,
                oil_status:oil_status,
                oil_remark:oil_remark,
                oil_id:$(".wrap_oil_set input[name = id]").val(),
            };

            $.ajax({
                url:common_ops.buildUrl("/oil/set"),
                type:"POST",
                data:data,
                dataType:"json",
                success:function (res) {
                    btn_traget.removeClass("disabled");
                    var callback = null;
                    if(res.code == 200){
                        callback = function () {
                            window.location.href =common_ops.buildUrl("/oil/index");
                        }
                    }
                    common_ops.alert(res.msg,callback);
                }
            });



        });
    }
}

$(document).ready( function () {
        oil_set_ops.init();
    }
);