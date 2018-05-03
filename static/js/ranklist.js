Vue.component('user-ranklist-table', {
    // user-info-table 组件现在接受一个
    // "prop"，类似于一个自定义特性。
    // 这个 prop 名为 todo。
    props: ['slist'],
    template: `
        <table class="ui celled selectable striped table">
            <thead>
            <tr>
                <th rowspan="2">排名</th>
                <th rowspan="2">学号</th>
                <th rowspan="2">姓名</th>
                <th>当前能力rating</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(item, index) in slist.slice((page_index-1)*page_size,page_index*page_size)">
                <td>{{ item.rank_id }}</td>
                <td>{{ item.userId }}</td>
                <td>{{ item.userName }}</td>
                <td>{{ item.rating }} <a style="font-size:13px;" :href="'/userInfo/' + item.userId + '#rank_list_charts'">详情</a></td>
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
            page_size: 20,
            page_length: Math.floor((this.slist.length + 20 - 1) / 20),
        }
    },
    watch: {
        slist: function (val, oldVal) {
            this.page_length = Math.floor((this.slist.length + this.page_size - 1) / this.page_size);
            this.page_index = 1;
        },
    },
    methods: {

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

});


$(document).ready(function () {
    new Vue({
        el: '#rank_list_table',
        data: {
            isActive: false,
            selected: -1,
            selectedlist: {},
            slist: [],
            searchlist: [],
            list: rank_list,
            page_size: 20,
            page_index: 1,
        },
        created() {
            this.setSlist(this.list);
        },
        methods: {
            // 获取需要渲染到页面中的数据
            setSlist(arr) {
                this.slist = JSON.parse(JSON.stringify(arr));
            },
            setList(arr) {
                this.list = arr;
                this.setSlist(this.list)
            },
            // 搜索
            search(e) {
                let v = e.target.value,
                    self = this;
                self.searchlist = [];
                if (v) {
                    let ss = [];
                    // 过滤需要的数据
                    this.list.forEach(function (item) {
                        if (item['userName'].indexOf(v) > -1) {
                            if (self.searchlist.indexOf(item.userName) == -1) {
                                self.searchlist.push(item.userName);
                            }
                            ss.push(item);
                        } else if (item['userId'] && item['userId'].indexOf(v) > -1) {
                            if (self.searchlist.indexOf(item.userId) == -1) {
                                self.searchlist.push(item.userId);
                            }
                            ss.push(item);
                        }
                    });
                    this.setSlist(ss); // 将过滤后的数据给了slist
                } else {
                    // 没有搜索内容，则展示全部数据
                    this.setSlist(this.list);
                }
            },

        },
        watch: {}
    })
});