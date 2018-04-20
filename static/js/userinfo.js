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

Vue.component('user-sub-info-table', {
    // user-info-table 组件现在接受一个
    // "prop"，类似于一个自定义特性。
    // 这个 prop 名为 todo。
    props: ['slist'],
    template: `
        <table class="ui fixed celled structured table">
            <thead>
            <tr>
                <th rowspan="2">学号</th>
                <th rowspan="2">姓名</th>
                <th rowspan="2">Oj</th>
                <th rowspan="2">ProblemId</th>
                <th rowspan="2">日期</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(item, index) in slist.slice((page_index-1)*page_size,page_index*page_size)">
                <td>{{ item.userId }}</td>
                <td>{{ item.userName }}</td>
                <td>{{ item.ojName }}</td>
                <td>{{ item.proId }}</td>
                <td>{{ item.acDate }}</td>
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
    const RARING_NAME = {
        1699: 'Pupil',
        2099: 'Specialist',
        2399: 'Expert',
        2699: 'Candidate Master',
        2999: 'Master',
        3399: 'GrandMaster',
        3899: 'International GrandMaster',
        9999: 'Legendary GrandMaster',
    };
    const RATING_NUMBER = [1699, 2099, 2399, 2699, 2999, 3399, 3899, 9999];

    let daily_info = {};
    let labelTop = {
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
    let labelFromatter = {
        normal: {
            label: {
                formatter: function (params) {
                    let oj_name = params.name.split(':WA')[0];
                    let subTimes = 0;
                    let acTimes = 0;
                    if (daily_info[oj_name]) {
                        subTimes = daily_info[oj_name][0].subTimes;
                        acTimes = daily_info[oj_name][0].acTimes;
                    }
                    let acRatio = subTimes ? (acTimes / subTimes * 100).toFixed(2) : 0;
                    return acTimes + '/' + subTimes + '(' + acRatio + '%)'
                },
                textStyle: {
                    baseline: 'top'
                }
            }
        },
    };
    let labelBottom = {
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
    let radius = [40, 55];
    let DATE_FORMAT = 'YYYY-MM-DD';

    function getRankName(rating) {
        for (let i = 0; i < RATING_NUMBER.length; i++) {
            let rating_top = RATING_NUMBER[i];
            if (rating_top > rating) {
                return RARING_NAME[rating_top]
            }
        }
        return 'International GrandMaster';
    }

    const user_id = window.location.href.split('/').pop().split('?')[0];
    const dailyInfoAcRatioOption = {
        backgroundColor: '#1b1c1d',
        legend: {
            x: 'center',
            y: 'center',
            data: OJ_NAME,
        },
        title: {
            text: 'Oj Accept Ratio',
            subtext: 'bower by zucc crawler',
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
            subtext: 'bower by zucc crawler',
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
    const weeklyInfoCountOption = {
        backgroundColor: '#1b1c1d',
        title: {
            text: '七日刷题曲线',
            subtext: 'power by zucc crawler'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['提交数', 'ac数']
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {
                    show: true, readOnly: true, optionToContent: function (opt) {
                        let axisData = opt.xAxis[0].data; //坐标数据
                        let series = opt.series; //折线图数据
                        let tdHeads = '<td  style="padding: 0 10px">时间</td>'; //表头
                        let tdBodys = ''; //数据
                        series.forEach(function (item) {
                            //组装表头
                            tdHeads += `<th>${item.name}</th>`;
                        });
                        let table = `<table class="ui selectable fixed compact celled table"><tbody><tr>${tdHeads} </tr>`;
                        for (let i = 0, l = axisData.length; i < l; i++) {
                            for (let j = 0; j < series.length; j++) {
                                //组装表数据
                                tdBodys += `<td>${ series[j].data[i]}</td>`;
                            }
                            table += `<tr><td>${axisData[i]}</td>${tdBodys}</tr>`;
                            tdBodys = '';
                        }
                        table += '</tbody></table>';
                        return table;
                    }
                },
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: []
            }
        ],
        yAxis: [
            {
                type: 'value',
                axisLabel: {
                    formatter: '{value}'
                }
            }
        ],
        series: [
            {
                name: 'ac数',
                type: 'line',
                barMaxWidth: 40,
                data: [],
                smooth: true,
                markPoint: {
                    data: [
                        {type: 'max', name: '周最高'},
                        {type: 'min', name: '周最低'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            },
            {
                name: '提交数',
                type: 'line',
                barMaxWidth: 40,
                data: [],
                smooth: true,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            }
        ]
    };
    const rankListChartOption = {
        chart: {
            renderTo: 'rank_list_charts',
            defaultSeriesType: 'line',
            backgroundColor: null
        },
        title: {
            text: '能力提升轨迹',
            style: {
                color: 'rgba(255,255,255,.9)!important',
            },
        },
        loading: {
            hideDuration: 500,
            labelStyle: {
                fontWeight: 'bold',
                position: 'relative',
                top: '1em'
            },
            showDuration: 500,
            style: {
                position: 'absolute',
                backgroundColor: null,
                opacity: 0.5,
                textAlign: 'center',
                color: 'rgba(255,255,255,.9)!important',
            }
        },
        xAxis: {
            type: 'datetime',
            dataTimeLabelFormats: {
                month: '%e. %b',
                year: '%b'
            },
            labels: {
                style: {
                    color: 'rgba(255,255,255,.9)!important',
                },
            },
        },
        yAxis: {
            title: {
                text: 'Rating',
                style: {
                    color: 'rgba(255,255,255,.9)!important',
                },
            },
            labels: {
                style: {
                    color: 'rgba(255,255,255,.9)!important',
                },
            },
            min: null,
            minorGridLineWidth: 100,
            gridLineWidth: 0,
            alternateGridColor: null,
            plotBands: [{
                from: 0,
                to: 1700,
                color: '#c3c3c3'
            }, {
                from: 1700,
                to: 2100,
                color: '#6cd8b3'
            }, {
                from: 2100,
                to: 2400,
                color: '#a0a0ff'
            }, {
                from: 2400,
                to: 2700,
                color: '#ff7dff'
            }, {
                from: 2700,
                to: 3000,
                color: '#ffbb55'
            }, {
                from: 3000,
                to: 3400,
                color: '#ff6b6c'
            }, {
                from: 3400,
                to: 3900,
                color: '#ff2c2d'
            }, {
                from: 3900,
                to: 99999,
                color: '#aa0200'
            }]
        },
        tooltip: {

            formatter: function () {
                return '<b>Rating</b>：' + this.y + '(' + this.point.change + ')' + '<br/>'
                    + '<b>Rank Title</b>：' + getRankName(this.y) + '<br/>'
                    + '<b>时间</b>：' + Highcharts.dateFormat('%Y-%m-%e', this.x) + '<br/>'
            }
        },
        plotOptions: {
            spline: {
                marker: {
                    radius: 4,
                    lineColor: '#666666',
                    lineWidth: 1
                }
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '参赛轨迹',
            marker: {symbol: 'square'},
            showInLegend: false,
            data: []
        }],
        navigation: {
            menuItemStyle: {
                fontSize: '10px'
            }
        }
    };

    let dailyInfoCharts = echarts.init($("#dailyInfo")[0], 'dark');
    let dailyAcRatioCharts = echarts.init($("#dailyAcRatioInfo")[0], 'dark');
    let weeklyInfoCountCharts = echarts.init($("#weeklyInfoCount")[0], 'dark');
    let rankInfoCharts = new Highcharts.Chart(rankListChartOption);
    rankInfoCharts.showLoading();
    $.get('/rank_list/' + user_id, null, function (response) {
        rankInfoCharts.hideLoading();
        if (response.status == 'ok') {
            let rank_info = [{
                'x': +moment('2018-04-17'),
                'y': 1500,
                'change': 0,
                'rating': 1500
            }].concat(response.result.rank_info);
            for (var i = 1; i < rank_info.length; i++) {
                rank_info[i]['x'] = +moment(rank_info[i]['countDate']);
                rank_info[i]['y'] = parseFloat(rank_info[i]['rating']);
                rank_info[i]['change'] = rank_info[i]['rating'] - (i > 0 ? rank_info[i - 1]['rating'] : 1500)
                rank_info[i]['rating'] = (rank_info[i]['rating'] >= 0 ? '+' : '') + rank_info[i]['rating']
            }
            rankListChartOption.series[0].data = rank_info;
            rankInfoCharts = new Highcharts.Chart(rankListChartOption);
        } else {
            alert('数据获取失败')
        }
    }, 'json');
    let converDailyCountData = function (p, key) {
        return $lodash.map(OJ_NAME, o => {
            return {
                name: o, value: (p[o] ? p[o][0][key]
                    : 0)
            }
        })
    };

    let converAcRatioData = function (opt, p) {
        $lodash.map(opt.series, o => {
            let oj_name = o.data[1].name;
            let subTimes = 1;
            let acTimes = 0;
            if (p[oj_name]) {
                subTimes = Math.max(p[oj_name][0].subTimes, 1);
                acTimes = p[oj_name][0].acTimes;
            }
            o.data[0].name = oj_name + ':WA';
            o.data[0].value = subTimes - acTimes;
            o.data[1].value = acTimes
        })
    };
    let edDay = moment();
    let stDay = moment().subtract(1, 'week');
    let pre_st, pre_ed;
    let is_show = false;
    let sub_info_list = [];
    pre_st = stDay.format(DATE_FORMAT);
    pre_ed = edDay.format(DATE_FORMAT);
    $('#st').val(pre_st);
    $('#ed').val(pre_ed);

    $(".ui.search.data.button").click(function () {
        let st = $('#st').val();
        let ed = $('#ed').val();
        if (st === "") st = null;
        if (ed === "") ed = null;
        let vaildSt = moment(st, DATE_FORMAT);
        let vaildEd = moment(ed, DATE_FORMAT);
        if (!vaildSt.isValid() || !vaildEd.isValid()) {
            alert('请输入正确的日期');
            $('#st').val(pre_st);
            $('#ed').val(pre_ed);
            return
        }
        if (st !== pre_st || ed !== pre_ed) {
            let stDate = moment(st, DATE_FORMAT);
            let edDate = moment(st, DATE_FORMAT).add(1, 'week').format(DATE_FORMAT);
            showWeeklyCount(stDate, edDate);
            searchSubInfo(st, ed);
            pre_st = st;
            pre_ed = ed;
        }
    });
    let searchSubInfo = function (st, ed) {
        $.ajax({
            type: 'POST',
            url: '/subInfo/search',
            timeout: 3000,
            contentType: 'application/json',
            data: JSON.stringify({
                'userId': user_id,
                'groupBy': false,
                'st': st,
                'ed': ed,
            }),
            dataType: 'json',
            success: function (data) {
                if (data.status != 'ok') {
                    alert('查询错误')
                }
                sub_info_list = data.result['sub_info'];
                user_sub_info_table.setList(sub_info_list)
            },
            error: function (xhr, type) {
                alert('error:' + type);
            }
        });
    };

    function showWeeklyCount(st, ed) {
        st = st || moment().subtract(1, 'week').format(DATE_FORMAT);
        ed = ed || moment().format(DATE_FORMAT);
        let date_array = [];
        for (let delta = 7; delta > 0; --delta) {
            let date = moment(ed, DATE_FORMAT).subtract(delta, 'day').format(DATE_FORMAT);
            date_array.push(date)
        }
        weeklyInfoCountOption.xAxis[0].data = date_array;
        $.ajax({
            type: 'POST',
            url: '/dailyInfo/search',
            timeout: 3000,
            contentType: 'application/json',
            data: JSON.stringify({
                'userId': user_id,
                'groupBy': false,
                'st': st,
                'ed': ed,
            }),
            dataType: 'json',
            success: function (data) {
                if (data.status != 'ok') {
                    alert('查询错误')
                }
                daily_info = data.result['daily_info'];
                daily_info = $lodash.groupBy(daily_info, o => o.countDate);
                let sub_info_array = [];
                let ac_info_array = [];
                $lodash.map(date_array, (date) => {
                    let acTimes = $lodash.sumBy(daily_info[date], o => o.acTimes);
                    let subTimes = $lodash.sumBy(daily_info[date], o => o.subTimes);
                    sub_info_array.push(subTimes);
                    ac_info_array.push(acTimes);
                });
                weeklyInfoCountOption.series[1].data = sub_info_array;
                weeklyInfoCountOption.series[0].data = ac_info_array;
                weeklyInfoCountCharts.setOption(weeklyInfoCountOption);
                if (is_show == false && is_crawler
                    && login_user_id == user_id
                    && $lodash.sum(sub_info_array) == 0
                    && moment().isAfter(moment(ed, DATE_FORMAT))) {
                    is_show = true;
                    alert('你已经一周没训练了')
                }
            },
            error: function (xhr, type) {
                alert('error:' + type);
            }
        });
    }

    showWeeklyCount();
    searchSubInfo(pre_st, pre_ed);
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
        weeklyInfoCountCharts.resize();
    });
    let userinfo_guide_menu = new Vue({
        el: "#userinfo-guide-menu",
        data: {
            infos: [{name: '题数与信息汇总', tag_id: 'dailyAcRatioInfo'}],
        },
        methods: {
            goto: (tag_id) => {
                $('html, body').animate({scrollTop: $(`#${tag_id}`).offset().top - 30}, 500,
                    () => {
                        let grade_offset = $(`#${tag_id}`).offset().top;
                        let menu_offset = $('#userinfo-guide-menu').offset().top;
                        if (menu_offset > grade_offset) {
                            $('html, body').animate({scrollTop: $(`#${tag_id}`).offset().top - 30}, 500)
                        }
                    })
            }
        }
    })
    if (login_user_id != 'anonymous') {
        userinfo_guide_menu.infos.push({name: '用户oj信息详情', tag_id: 'user_oj_info_table'});
        new Vue({
            el: '#user_oj_info_table',
            data: {
                isActive: false,
                selected: -1,
                selectedlist: {},
                slist: [],
                searchlist: [],
                list: user_oj_info.items,
                user_id: user_oj_info.user_id,
                user_name: user_oj_info.user_name,
            },
            created() {
                this.setSlist(this.list);
            },
            methods: {
                // 获取需要渲染到页面中的数据
                setSlist(arr) {
                    this.slist = JSON.parse(JSON.stringify(arr));
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
                            if (item['oj_name'].indexOf(v) > -1) {
                                if (self.searchlist.indexOf(item.oj_name) == -1) {
                                    self.searchlist.push(item.oj_name);
                                }
                                ss.push(item);
                            } else if (item['user_oj_id'] && item['user_oj_id'].indexOf(v) > -1) {
                                if (self.searchlist.indexOf(item.user_oj_id) == -1) {
                                    self.searchlist.push(item.user_oj_id);
                                }
                                ss.push(item);
                            } else if (item['user_name'].indexOf(v) > -1) {
                                if (self.searchlist.indexOf(item.user_name) == -1) {
                                    self.searchlist.push(item.user_name);
                                }
                                ss.push(item);
                            } else if (item['user_id'].indexOf(v) > -1) {
                                if (self.searchlist.indexOf(item.user_id) == -1) {
                                    self.searchlist.push(item.user_id);
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
        });
    }
    let user_sub_info_table = new Vue({
        el: '#user_sub_info_table',
        data: {
            isActive: false,
            selected: -1,
            selectedlist: {},
            slist: [],
            searchlist: [],
            list: sub_info_list,
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
                        if (item['ojName'].indexOf(v) > -1) {
                            if (self.searchlist.indexOf(item.ojName) == -1) {
                                self.searchlist.push(item.oj_name);
                            }
                            ss.push(item);
                        } else if (item['acDate'] && item['acDate'].indexOf(v) > -1) {
                            if (self.searchlist.indexOf(item.acDate) == -1) {
                                self.searchlist.push(item.acDate);
                            }
                            ss.push(item);
                        } else if (item['proId'] && item['proId'].indexOf(v) > -1) {
                            if (self.searchlist.indexOf(item.acDate) == -1) {
                                self.searchlist.push(item.acDate);
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
    userinfo_guide_menu.infos.push({name: '能力提升轨迹', tag_id: 'rank_list_charts'});
    userinfo_guide_menu.infos.push({name: '七日做题曲线', tag_id: 'weeklyInfoCount'});
    userinfo_guide_menu.infos.push({name: '题目详情列表', tag_id: 'user_sub_info_table'});
    $('.ui.sticky')
        .sticky();
});