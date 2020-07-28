/**
 * Created by Administrator on 2018-09-12.
 */
;
var equip_set_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $(".wrap_equip_set .save").click(function () {

            var btn_traget = $(this);
            if(btn_traget.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交")
                return;
            }
            //参数获取部分
            // 设备编号
            var equip_id_target = $(".wrap_equip_set input[name = equip_id]");
            var equip_id = equip_id_target.val();
            // 所属钻井平台
            var equip_platform_target = $(".wrap_equip_set select[name = equip_platform]");
            var equip_platform = equip_platform_target.val();
            // 监测油品
            var equip_oil_target = $(".wrap_equip_set select[name = equip_oil]");
            var equip_oil = equip_oil_target.val();
            // 罐体长度
            var equip_length_target = $(".wrap_equip_set input[name = equip_length]");
            var equip_length = equip_length_target.val();
            // 罐体宽度
            var equip_width_target = $(".wrap_equip_set input[name = equip_width]");
            var equip_width = equip_width_target.val();
            // 罐体高度
            var equip_height_target = $(".wrap_equip_set input[name = equip_height]");
            var equip_height = equip_height_target.val();
            // 设备状态
            var equip_status_target = $(".wrap_equip_set select[name = equip_status]");
            var equip_status = equip_status_target.val();
            // 备注信息
            var equip_remark_target = $(".wrap_equip_set input[name = equip_remark]");
            var equip_remark = equip_remark_target.val();


            // 参数校验部分
            if( equip_id.length < 1)
            {
                common_ops.tip("请输入符合规范的设备编号！",equip_id_target);
                return false;
            }
            if(equip_platform.length < 1)
            {
                common_ops.tip("请选择钻井平台！",equip_platform_target);
                return false;
            }
            if(equip_oil.length < 1)
            {
                common_ops.tip("请选择监测油品！",equip_oil_target);
                return false;
            }
            if(equip_length.length < 1)
            {
                common_ops.tip("请输入符合规范的罐体长度！",equip_length_target);
                return false;
            }
            if(equip_width.length < 1)
            {
                common_ops.tip("请输入符合规范的罐体宽度！",equip_width_target);
                return false;
            }
            if(equip_height.length < 1)
            {
                common_ops.tip("请输入符合规范的罐体高度！",equip_height_target);
                return false;
            }
            if(equip_status.length < 1)
            {
                common_ops.tip("请输入符合规范的设备状态！",equip_status_target);
                return false;
            }
            if(equip_remark.length < 1)
            {
                common_ops.tip("请输入符合规范的备注信息！",equip_status_target);
                return false;
            }

            btn_traget.addClass("disabled");

            var data = {
                equip_platform:equip_platform,
                equip_oil:equip_oil,
                equip_length:equip_length,
                equip_width:equip_width,
                equip_height:equip_height,
                equip_status:equip_status,
                equip_remark:equip_remark,
                equip_id:$(".wrap_equip_set input[name = equip_id]").val(),
            };

            $.ajax({
                url:common_ops.buildUrl("/equip/set"),
                type:"POST",
                data:data,
                dataType:"json",
                success:function (res) {
                    btn_traget.removeClass("disabled");
                    var callback = null;
                    if(res.code == 200){
                        callback = function () {
                            window.location.href =common_ops.buildUrl("/equip/index");
                        }
                    }
                    common_ops.alert(res.msg,callback);
                }
            });

        });
    }
}

$(document).ready( function () {
        equip_set_ops.init();
    }
);