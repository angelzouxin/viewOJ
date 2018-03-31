Vue.component('user-manager-table', {
        props: ['slist', 'head_names'],
        template: `
        <table class="ui selectable compact celled definition table" id="table">
            <thead>
            <tr>
                    <th v-for="head_name in head_names">{{ head_name }}</th>
            </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in slist.slice((page_index-1)*page_size,page_index*page_size)">
                    <td id="userId">{{ item.userId }}</td>
                    <td><input v-if="item.edit" @keyup.enter="changeUserName(index)" v-model="item.change_user_name">
                        <span v-if="!item.edit">{{ item.userName }}<span style="margin-left: 5px"><i
                            class="edit icon" @click="editing(index)"></i></span></span>
                    </td>
                    <td id="check">
                        <div class="collapsing">
                            <div class="ui fitted slider checkbox">
                                <input @click="changeYN(index);" type="checkbox" :checked="item.yn == 1">
                                <label></label>
                            </div>
                        </div>
                    </td>
                    <td id="permission">
                        <selected-drop-down
                            :list="[{id: 0, name: 'admin'},{id: 1, name: 'student'}]"
                            :value="item.permission"
                            :defaultText="item.permission"
                            @valueChanged="updatePermission(index, $event)">
                        </selected-drop-down>
                    </td>
                    <td>
                        <a id="userInfo" @click="getUserInfo(index)">详情</a>
                    </td>
                </tr>
            </tbody>
        <tfoot class="full-width">
        <tr>
            <th></th>
            <th colspan="4">
                <div class="ui center floated pagination menu">
                    <a :class="(page_index == 1 ? 'disabled' : '') + ' icon item'" @click="leftPage" :disabled="page_index == 1">
                        <i class="left chevron icon"></i>
                    </a>
                    <a @click="if (item_index != '...') page_index=item_index" :class="(page_index == item_index ? 'active' : '') + ' item'" v-for="item_index in changePageList">{{ item_index | showPage }}</a>
                    <a :class="(page_index == page_length ? 'disabled' : '') + ' icon item'" @click="rightPage" :disabled="page_index == page_length">
                        <i class="right chevron icon"></i>
                    </a>
                </div>
                <div class="ui right floated small primary labeled icon add user button">
                    <i class="user icon"></i>
                    添加用户
                </div>
            </th>
        </tr>
        </tfoot>
    </table>
        `,
        methods: {
            editing(index) {
                for (let [item_index, item] of
                    this.slist.slice((this.page_index - 1) * this.page_size, this.page_index * this.page_size).entries()) {
                    item.edit = item_index == index
                    item.change_user_name = item.userName
                }
            },

            leftPage() {
                if (this.page_index > 1)
                    --this.page_index
            },

            rightPage() {
                if (this.page_index < Math.floor((this.slist.length + this.page_size - 1) / this.page_size))
                    ++this.page_index
            },

            changeYN(index) {
                let item = this.slist[(this.page_index - 1) * this.page_size + index];
                let yn = !item.yn;
                let user_id = item.userId;
                $.ajax({
                    type: 'POST',
                    url: '/user/update',
                    timeout: 3000,
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'userId': user_id,
                        'yn': yn,
                    }),
                    dataType: 'json',
                    success: function (data) {
                        if (data.result) {
                            alert('更新成功');
                            item.yn = !item.yn;
                            user_list[item.item_index].yn = item.yn
                        } else {
                            alert('更新失败');
                        }
                    },
                    error: function (xhr, type) {
                        alert('error:' + type);
                    }
                });
            },

            changeUserName(index) {
                let item = this.slist[(this.page_index - 1) * this.page_size + index];
                let user_id = item.userId;
                let user_name = item.userName;
                let user_input = item.change_user_name;

                if (user_name == user_input) {
                    item.edit = false;
                    return
                }
                $.ajax({
                    type: 'POST',
                    url: '/user/update',
                    timeout: 2000,
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'userId': user_id,
                        'userName': user_input,
                    }),
                    dataType: 'json',
                    success: function (data) {
                        if (data.result) {
                            item.userName = user_input;
                            item.edit = false;
                            user_list[item.item_index].userName = user_input;
                            alert('更新成功');
                        } else {
                            alert('更新失败');
                        }
                    },
                    error: function (xhr, type) {
                        alert('error:' + type);
                    }
                });
            },

            getUserInfo(index) {
                let item = this.slist[(this.page_index - 1) * this.page_size + index];
                let user_id = item.userId;
                window.location.href = 'userInfo/' + user_id
            },

            updatePermission(index, permission) {
                let item = this.slist[(this.page_index - 1) * this.page_size + index];
                let userId = item.userId;
                let change_permission = permission;
                $.ajax({
                    type: 'POST',
                    url: '/user/update',
                    timeout: 3000,
                    contentType: 'application/json',
                    data: JSON.stringify({
                        'userId': userId,
                        'permission': change_permission,
                    }),
                    dataType: 'json',
                    success: function (data) {
                        if (data.result) {
                            item.permission = change_permission;
                            user_list[item.item_index].permission = change_permission;
                            alert('更新成功');
                        } else {
                            alert('更新失败');
                        }
                    },
                    error: function (xhr, type) {
                        alert('error:' + type);
                    }
                });
            }
        },
        data: function () {
            return {
                page_index: 1,
                page_size: 12,
                page_length: Math.floor((this.slist.length + 12 - 1) / 12),
            }
        },
        computed: {
            changePageList: function () {
                let val = this.page_index;
                let list = [];
                if (this.page_length < 10) {
                    list = [...Array(this.page_length + 1).keys()].slice(1)
                } else {
                    if (val > 3) {
                        list.push('...')
                    }
                    let min_page = Math.max(1, val - 2);
                    let max_page = Math.min(this.page_length - 1, val + 2);
                    for (let i = min_page; i <= max_page; i++) {
                        list.push(i)
                    }
                    if (max_page < this.page_length - 1) {
                        list.push('...')
                    }
                    list.push(this.page_length)
                }
                return list
            }
        },
        watch: {
            slist: function (val, oldVal) {
                this.page_length = Math.floor((this.slist.length + this.page_size - 1) / this.page_size);
                this.page_index = 1;
            },
        },
    }
);

Vue.component('selected-drop-down', {
    props: ["defaultText", "list", "value"],
    template: `
        <div class="ui selection dropdown semanticDropDown">
            <input type="hidden" :value="value"  @change="updateDropdown">
            <i class="dropdown icon"></i>
            <div class="text">{{ defaultText }}</div>
            <div class="menu">
                <div v-for="item in items" class="item" :data-value="item.id">{{ item.name }}</div>
            </div>
        </div>
    `,
    created() {
        this.items = this.list
    },
    watch: {
        value: function (val, oldVal) {
            if (val == null) {
                $(this.$el).dropdown('clear');
            }
            if (val != oldVal) {
                $(this.$el).dropdown('set selected', val);
            }
        },
        items: function (val, oldVal) {
            $(this.$el).dropdown('refresh');
        }
    },
    methods: {
        updateDropdown() {
            let id_value = $(this.$el).find('input').val();
            id_value = (id_value === "" || id_value === null) ? '' : id_value;
            if (this.defaultText == this.items[id_value].name) {
                return
            }
            this.$emit('input', id_value);
            this.$emit('valueChanged', this.items[id_value].name);
        }
    },
    data: function () {
        return {
            innerItems: this.items,
            selected: '',
            selecteditem: {},

        };
    },
    mounted() {
        $(this.$el).dropdown();
    },
})

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
});

