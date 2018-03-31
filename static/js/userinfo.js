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

});

$(document).ready(function () {
    const OJ_NAME = [
        'hdu', 'poj', 'zoj', 'CODEVS', 'bzoj',
        'codeforces', 'SJTUOJ', 'vjudge', 'ural', 'spoj', 'zucc'
    ];
    var daily_info = {};
    var labelTop = {
        normal: {
            label: {
                show: true,
                position: 'center',
                formatter: '{b}',
                textStyle: {
                    baseline: 'bottom'
                }
            },
            labelLine: {
                show: false
            }
        }
    };
    var labelFromatter = {
        normal: {
            label: {
                formatter: function (params) {
                    var oj_name = params.name.split(':WA')[0];
                    var subTimes = 0;
                    var acTimes = 0;
                    if (daily_info[oj_name]) {
                        subTimes = daily_info[oj_name][0].subTimes;
                        acTimes = daily_info[oj_name][0].acTimes;
                    }
                    var acRatio = subTimes ? (acTimes/subTimes*100).toFixed(2) : 0;
                    return acTimes + '/' + subTimes + '(' + acRatio + '%)'
                },
                textStyle: {
                    baseline: 'top'
                }
            }
        },
    };
    var labelBottom = {
        normal: {
            color: '#ccc',
            label: {
                show: true,
                position: 'center'
            },
            labelLine: {
                show: false
            }
        },
        emphasis: {
            color: 'rgba(0,0,0,0)'
        }
    };
    var radius = [40, 55];

    const user_id = window.location.href.split('/').pop().split('?')[0]
    const dailyInfoAcRatioOption = {
        backgroundColor: '#1b1c1d',
        legend: {
            x: 'center',
            y: 'center',
            data: OJ_NAME,
        },
        title: {
            text: 'Oj Accept Ratio',
            subtext: 'bower by zucc crawel',
            x: 'center',
            textStyle: {
                color: '#fff'
            }
        },
        toolbox: {
            show: true,
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {
                    show: true,
                    type: ['pie', 'funnel'],
                    option: {
                        funnel: {
                            width: '20%',
                            height: '30%',
                            itemStyle: {
                                normal: {
                                    label: {
                                        formatter: function (params) {
                                            return 'other\n' + params.value + '%\n'
                                        },
                                        textStyle: {
                                            baseline: 'middle'
                                        }
                                    }
                                },
                            }
                        }
                    }
                },
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        series: [
            {
                type: 'pie',
                center: ['20%', '30%'],
                radius: radius,
                x: '0%', // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 46, itemStyle: labelBottom},
                    {name: 'hdu', value: 54, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['35%', '30%'],
                radius: radius,
                x: '20%', // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 56, itemStyle: labelBottom},
                    {name: 'poj', value: 44, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['50%', '30%'],
                radius: radius,
                x: '40%', // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 65, itemStyle: labelBottom},
                    {name: 'zoj', value: 35, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['65%', '30%'],
                radius: radius,
                x: '60%', // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 70, itemStyle: labelBottom},
                    {name: 'CODEVS', value: 30, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['80%', '30%'],
                radius: radius,
                x: '80%', // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 73, itemStyle: labelBottom},
                    {name: 'bzoj', value: 27, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['12.5%', '70%'],
                radius: radius,
                y: '55%',   // for funnel
                x: '0%',    // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 78, itemStyle: labelBottom},
                    {name: 'codeforces', value: 22, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['27.5%', '70%'],
                radius: radius,
                y: '55%',   // for funnel
                x: '20%',    // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 78, itemStyle: labelBottom},
                    {name: 'SJTUOJ', value: 22, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['42.5%', '70%'],
                radius: radius,
                y: '55%',   // for funnel
                x: '40%', // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 78, itemStyle: labelBottom},
                    {name: 'vjudge', value: 22, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['57.5%', '70%'],
                radius: radius,
                y: '55%',   // for funnel
                x: '60%', // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 83, itemStyle: labelBottom},
                    {name: 'ural', value: 17, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['72.5%', '70%'],
                radius: radius,
                y: '55%',   // for funnel
                x: '80%', // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 89, itemStyle: labelBottom},
                    {name: 'spoj', value: 11, itemStyle: labelTop}
                ]
            },
            {
                type: 'pie',
                center: ['87.5%', '70%'],
                radius: radius,
                y: '55%',   // for funnel
                x: '80%', // for funnel
                itemStyle: labelFromatter,
                data: [
                    {name: 'other', value: 89, itemStyle: labelBottom},
                    {name: 'zucc', value: 11, itemStyle: labelTop}
                ]
            }
        ]
    };
    const dailyInfoCountOption = {
        backgroundColor: '#1b1c1d',
        title: {
            text: '题数汇总',
            subtext: 'bower by zucc crawel',
            x: 'center',
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data: OJ_NAME
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: true},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,
        series: [
            {
                name: 'OJ名称',
                type: 'pie',
                radius: '35%',
                center: ['50%', '60%'],

                data: []
            },
        ]
    };

    var dailyInfoCharts = echarts.init($("#dailyInfo")[0], 'dark');
    var dailyAcRatioCharts = echarts.init($("#dailyAcRatioInfo")[0], 'dark');
    var converDailyCountData = function (p, key) {
        return $lodash.map(OJ_NAME, o => {
            return {
                name: o, value: (p[o] ? p[o][0][key]
                    : 0)
            }
        })
    };

    var converAcRatioData = function (opt, p) {
        $lodash.map(opt.series, o => {
            var oj_name = o.data[1].name;
            var subTimes = 1;
            var acTimes = 0;
            if (p[oj_name]) {
                subTimes = Math.max(p[oj_name][0].subTimes, 1);
                acTimes = p[oj_name][0].acTimes;
            }
            o.data[0].name = oj_name + ':WA';
            o.data[0].value = subTimes - acTimes;
            o.data[1].value = acTimes
        })
    };

    $.ajax({
        type: 'POST',
        url: '/dailyInfo/search',
        timeout: 3000,
        contentType: 'application/json',
        data: JSON.stringify({
            'userId': user_id,
            'groupBy': true,
        }),
        dataType: 'json',
        success: function (data) {
            if (data.status != 'ok') {
                alert('查询错误')
            }
            daily_info = data.result['daily_info'];
            daily_info = $lodash.groupBy(daily_info, o => o.ojName);
            dailyInfoCountOption.series[0].data = converDailyCountData(daily_info, 'subTimes');
            dailyInfoCharts.setOption(dailyInfoCountOption);
            converAcRatioData(dailyInfoAcRatioOption, daily_info);
            dailyAcRatioCharts.setOption(dailyInfoAcRatioOption)
        },
        error: function (xhr, type) {
            alert('error:' + type);
        }
    });

    $(window).resize(function () {
        dailyInfoCharts.resize();
        dailyAcRatioCharts.resize();
    });

});