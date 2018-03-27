Vue.component('user-info-table', {
    // user-info-table 组件现在接受一个
    // "prop"，类似于一个自定义特性。
    // 这个 prop 名为 todo。
    props: ['slist', 'user_id', 'user_name'],
    template: `
        <table class="ui celled structured table">
            <thead>
            <tr>
                <th rowspan="2">学号</th>
                <th rowspan="2">姓名</th>
                <th colspan="2">Oj信息</th>
            </tr>
            <tr>
                <th>Oj</th>
                <th>用户id</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(item, index) in slist">
                <td>{{ user_id }}</td>
                <td>{{ user_name }}</td>
                <td>{{ item.oj_name }}</td>
                <td>
                    <input v-if="item.edit" @keyup.enter="update(index)" v-model="item.change_user_oj_id">
                    <span v-if="!item.edit">{{ item.user_oj_id }}<span style="margin-left: 5px"><i
                            class="edit icon" @click="editing(index)"></i></span></span>
                </td>
            </tr>
            </tbody>
        </table>
  `,
    methods: {
        editing(index) {
            for (let [item_index, item] of this.slist.entries()) {
                item.edit = item_index == index
                item.change_user_oj_id = item.user_oj_id
            }
        },

        update(index) {
            let item = this.slist[index]
            item.edit = false
            let update_info = item.change_user_oj_id
            if (update_info == item.user_oj_id) {
                return
            }
            if (!update_info || update_info == '') {
                alert('用户id不能为空')
                item.change_user_oj_id = item.user_oj_id
                return
            }
            $.ajax({
                type: 'POST',
                url: '/userInfo/update',
                timeout: 3000,
                contentType: 'application/json',
                data: JSON.stringify({
                    origin: this.slist[index],
                    user_oj_id: update_info,
                }),
                dataType: 'json',
                success: function (data) {
                    if (data.status == 'error') {
                        alert('用户id更新失败，' + data.message)
                        return
                    }
                    item.user_oj_id = update_info
                    user_oj_info.items[item.item_index].user_oj_id = update_info
                },
                error: function (xhr, type) {
                    alert('error:' + type);
                }
            })
        },
    }

})