/**
 * Created by Administrator on 2018-09-12.
 */
;
var platform_set_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $(".wrap_platform_set .save").click(function () {

            var btn_traget = $(this);
            if(btn_traget.hasClass("disabled")){
                common_ops.alert("正在处理！请不要重复提交")
                return;
            }
            //参数获取部分
            // 平台所属省份
            var platform_province_target = $(".wrap_platform_set input[name = platform_province]");
            var platform_province = platform_province_target.val();
            // 平台所属城市
            var platform_city_target = $(".wrap_platform_set input[name = platform_city]");
            var platform_city = platform_city_target.val();
            // 平台所属区县
            var platform_country_target = $(".wrap_platform_set input[name = platform_country]");
            var platform_country = platform_country_target.val();
            // 平台编号
            var platform_num_target = $(".wrap_platform_set input[name = platform_num]");
            var platform_num = platform_num_target.val();
            // 平台使用状态
            var platform_status_target = $(".wrap_platform_set select[name = platform_status]");
            var platform_status = platform_status_target.val();
            // 备注信息
            var platform_remark_target = $(".wrap_platform_set input[name = platform_remark]");
            var platform_remark = platform_remark_target.val();


            // 参数校验部分
            if( platform_province.length < 1)
            {
                common_ops.tip("请输入符合规范的省份！",platform_province_target);
                return false;
            }
            if(platform_city.length < 1)
            {
                common_ops.tip("请输入符合规范的城市！",platform_city_target);
                return false;
            }
            if(platform_country.length < 1)
            {
                common_ops.tip("请输入符合规范的区县！",platform_country_target);
                return false;
            }
            if(platform_num.length < 1)
            {
                common_ops.tip("请输入符合规范的编号！",platform_num_target);
                return false;
            }
            if(platform_status.length < 1)
            {
                common_ops.tip("请输入符合规范的状态！",platform_status_target);
                return false;
            }
            if(platform_remark.length < 1)
            {
                common_ops.tip("请输入符合规范的备注信息！",platform_remark_target);
                return false;
            }

            btn_traget.addClass("disabled");

            var data = {
                platform_province:platform_province,
                platform_city:platform_city,
                platform_country:platform_country,
                platform_num:platform_num,
                platform_status:platform_status,
                platform_remark:platform_remark,
                platform_id:$(".wrap_platform_set input[name = id]").val(),
            };

            $.ajax({
                url:common_ops.buildUrl("/platform/set"),
                type:"POST",
                data:data,
                dataType:"json",
                success:function (res) {
                    btn_traget.removeClass("disabled");
                    var callback = null;
                    if(res.code == 200){
                        callback = function () {
                            window.location.href =common_ops.buildUrl("/platform/index");
                        }
                    }
                    common_ops.alert(res.msg,callback);
                }
            });



        });
    }
}

$(document).ready( function () {
        platform_set_ops.init();
    }
);