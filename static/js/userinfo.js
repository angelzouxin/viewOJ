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
            <tr v-for="(item, index) in slist.slice((page_index-1)*page_size,page_index*page_size)">
                <td>{{ item.user_id }}</td>
                <td>{{ item.user_name }}</td>
                <td>{{ item.oj_name }}</td>
                <td>
                    <input v-if="item.edit" @keyup.enter="update(index)" v-model="item.change_user_oj_id">
                    <span v-if="!item.edit">{{ item.user_oj_id }}<span style="margin-left: 5px"><i
                            class="edit icon" @click="editing(index)"></i></span></span>
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
                </th>
            </tr>
            </tfoot>
        </table>
  `,
    data: function () {
        return {
            page_index: 1,
            page_size: 12,
            page_length: Math.floor((this.slist.length + 12 - 1) / 12),
        }
    },
    watch: {
        slist: function (val, oldVal) {
            this.page_length = Math.floor((this.slist.length + this.page_size - 1) / this.page_size);
            this.page_index = 1;
        },
    },
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

        leftPage() {
            if (this.page_index > 1)
                --this.page_index
        },

        rightPage() {
            if (this.page_index < Math.floor((this.slist.length + this.page_size - 1) / this.page_size))
                ++this.page_index
        },

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
    }

})