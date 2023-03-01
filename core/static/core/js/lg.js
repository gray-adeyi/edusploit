$("[name='login']").click(function (e) {
    let valid = true;
    $('#login_form [required]').each(function () {
        if ($(this).is(':invalid') || !$(this).val()) { valid = false; }
    })
    if (valid) {
        // e.preventDefault();
        $("#login").attr('disabled', true).html('loading <i class="fa fa-spinner fa-spin"></i>');
    }
});


$("[name='reg']").click(function (e) {
    let valid = true;
    $('#reg_form [required]').each(function () {
        if ($(this).is(':invalid') || !$(this).val()) { valid = false; }
    })
    if (valid) {
        e.preventDefault();
        var form = $("#reg_form")[0];
        var formData = new FormData(form);
        formData.append('reg', 1);
        $("#reg").attr('disabled', true).html('loading <i class="fa fa-spinner fa-spin"></i>');
        $.ajax({
            url: $("[name='reg_form']").attr('action'),
            data: formData,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function (d) {
                $("#reg").attr('disabled', false).html('CREATE <i class="fa fa-sign-in pull-right"></i>');
                $("#notification").html(d);
            },
            error: function (jqKHR, textStatus, errorThrown) {
                swal({ text: textStatus + ", Try Again!", type: 'warning', icon: 'warning' });
            }
        });
    }
});


toastr.options.showEasing = "swing";
toastr.options.closeButton = true;
toastr.options.closeEasing = 'swing';
toastr.options.positionClass = "toast-bottom-right";
toastr.options.showMethod = 'slideDown';
toastr.options.hideMethod = 'slideUp';
toastr.options.closeMethod = 'slideLeft';
toastr.options.progressBar = true;
toastr.options.timeOut = 3000;

function showpassword(id) {
    var psd1 = $("#psd1").val();
    if (psd1 == 0) {
        $("#password").attr("type", "text").focus();
        $("#showpassword").html('<i class="fa fa-eye-slash" ></i>');
        $("#psd1").val('1');
    } else {
        $("#password").attr("type", "password").focus();
        $("#showpassword").html('<i class="fa fa-eye" ></i>');
        $("#psd1").val('0');
    }
}

function showpassword2(id) {
    var psd2 = $("#psd2").val();
    if (psd2 == 0) {
        $("#password2").attr("type", "text").focus();
        $("#showpassword2").html('<i class="fa fa-eye-slash" ></i>');
        $("#psd2").val('1');
    } else {
        $("#password2").attr("type", "password").focus();
        $("#showpassword2").html('<i class="fa fa-eye" ></i>');
        $("#psd2").val('0');
    }
}



$(document).ready(function () {
    $('#email2').bind("cut copy paste", function (e) {
        e.preventDefault();
    });
});