$(document).ready(function () {
    $('.ui.add.user.button').click(function () {
        $('.ui.add.user.modal').modal('show');
    });

    $('form .ui.dropdown')
        .dropdown();

    $('.ui.clear.form.button').click(function () {
        $('.ui.form').form('clear')
    });

    $('.ui.check.form.button').click(function () {
        $('.ui.user.submit.button').click();
        return false
    });

    $('.ui.form')
        .form({
            inline: true,
            on: 'blur',
            fields: {
                name: {
                    identifier: 'userId',
                    rules: [
                        {
                            type: 'empty',
                            prompt: 'Please enter your userId'
                        }
                    ]
                },
                permission: {
                    identifier: 'permission',
                    rules: [
                        {
                            type: 'empty',
                            prompt: 'Please select a permission'
                        }
                    ]
                },
                username: {
                    identifier: 'userName',
                    rules: [
                        {
                            type: 'empty',
                            prompt: 'Please enter a username'
                        }
                    ]
                },
            }
        });

    $('.ui.permission.dropdown')
        .dropdown({
            onChange: function (permission) {
                let result = false
                let userId = this.parentNode.parentNode.cells[0].innerHTML;
                $.ajax({
                    async: false,
                    type: 'POST',
                    url: '/user/update',
                    timeout: 3000,
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'userId': userId,
                        'permission': permission,
                    }),
                    dataType: 'json',
                    success: function (data) {
                        if (data.result) {
                            result = true
                            alert('更新成功');
                        } else {
                            alert('更新失败');
                        }
                    },
                    error: function (xhr, type) {
                        alert('error:' + type);
                    }
                });
                return result
            }
        })
});

