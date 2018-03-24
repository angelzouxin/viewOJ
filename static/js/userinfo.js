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
                    <input v-if="item.edit" @keyup.enter="update(index)" v-model="item.user_oj_id">
                    <span v-if="!item.edit">{{ item.user_oj_id }}<span style="margin-left: 5px"><i
                            class="edit icon" @click="editing(index)"></i></span></span>
                </td>
            </tr>
            </tbody>
        </table>
  `,
    methods: {
        editing(index) {
            for(let [item_index, item] of this.slist.entries()) {
                item.edit = item_index == index
            }
        },

        update(index) {
            alert(this.slist[index].user_oj_id)
            this.slist[index].edit = false
        },
    }

})