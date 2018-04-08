$(document).ready(function () {

    let grades = {};

    let option = {
        backgroundColor: '#1b1c1d',
        title: {
            text: '增量图',
            textStyle: {
                fontWeight: 'normal',              //标题颜色
                color: '#ffffff'
            },
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {
                    show: true, readOnly: true,
                    optionToContent: function (opt) {
                        let axisData = opt.xAxis[0].data; //坐标数据
                        let series = opt.series; //折线图数据
                        let tdHeads = '<td  style="padding: 0 10px">用户</td>'; //表头
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
                magicType: {show: true, type: ['stack']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,
        tooltip: {},
        legend: {
            data: ['accept', 'submission'],
            textStyle: {
                color: '#ffffff'
            },
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            triggerEvent: true,
            data: [], axisLabel: {
                interval: 0, rotate: '-20', textStyle: {
                    color: '#fff',
                }
            },
        },
        yAxis: {
            axisLabel: {
                textStyle: {
                    color: '#fff',
                }
            },
        },
        series: [{
            name: 'accept',
            type: 'bar',
            barMaxWidth: 40,
            data: [],
            markLine: {
                data: [
                    {type: 'average', name: '平均值'},
                    {type: 'max'},
                    {type: 'min'}
                ]
            },
        }, {
            name: 'submission',
            type: 'bar',
            barMaxWidth: 40,
            data: [],
            barGap: '0%',
        }]
    };

    let pre_st, pre_ed;

    let charts = [];

    let echartClick = function(params) {
        if (params.componentType == 'xAxis') {
            let user_id = params.value.split(',')[0];
            window.location.href = 'userInfo/' + user_id;
        }
    };

    $(".ui.search.data.button").click(function () {
        let st = $('#st').val();
        let ed = $('#ed').val();
        if (st === "") st = null;
        if (ed === "") ed = null;
        if (st !== pre_st || ed !== pre_ed) {
            searchByDate(st, ed);
            pre_st = st;
            pre_ed = ed;
        }
    });

    let searchByDate = function (st, ed) {
        $.ajax({
            type: 'POST',
            url: '/search',
            timeout: 3000,
            contentType: 'application/json',
            data: JSON.stringify({
                'st': st,
                'ed': ed,
            }),
            dataType: 'json',
            success: function (data) {
                grades = {};
                chart_guide_menu.grades = [];
                $.each(data['dates'], function (idx, info) {

                    let grade = info['userId'].substr(0, 4);
                    let userId = info['userId'] + ',' + info['userName'];

                    let acTimes = 0;
                    let subTimes = 0;

                    $.each(info['dailyInfo'], function (idx, daily) {
                        acTimes += Number(daily['acTimes']);
                        subTimes += Number(daily['subTimes']);
                    });

                    if (grades[grade] === undefined) {
                        grades[grade] = [];
                    }

                    grades[grade].push({userId: userId, acTimes: acTimes, subTimes: subTimes})

                });

                $("#chart").empty();
                charts = []
                $.each(grades, function (grade, info) {

                    let option_grade = $.extend(true, {}, option);

                    option_grade.title.text = option_grade.title.text + grade;

                    $.each(info, function (idx, x) {
                        option_grade.xAxis.data.push(x['userId']);
                        option_grade.series[0].data.push(x['acTimes']);
                        option_grade.series[1].data.push(x['subTimes']);
                    });

                    $("#chart").append("<div id = " + grade + " style=\"width: 100%;height:780px;margin-top:50px;\"></div>");
                    $("#chart").append("<div class=\"ui divider\"></div>");
                    let myChart = echarts.init($("#" + grade).get(0));
                    myChart.setOption(option_grade);
                    myChart.on('click', echartClick)
                    charts.push(myChart)
                    chart_guide_menu.grades.push(grade)
                });

                $('.ui.sticky')
                    .sticky();
            },
            error: function (xhr, type) {
                alert('error:' + type);
            }
        });
    };
    let edDay = new Date();
    let stDay = new Date();
    stDay.setDate(stDay.getDate() - 7);
    pre_st = stDay.toJSON().substr(0, 10);
    pre_ed = edDay.toJSON().substr(0, 10);
    $('#st').val(pre_st);
    $('#ed').val(pre_ed);
    searchByDate(pre_st, pre_ed);
    $(window).resize(function () {
        $lodash.map(charts, o => o.resize())
    });
});