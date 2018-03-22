$(document).ready(function () {

    var grades = {};

    option = {
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
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['stack', 'tiled']},
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
            data: [],
            barGap: '0%',
        }]
    };

    var options = [];

    var pre_st, pre_ed;

    $(".ui.search.data.button").click(function () {
        var st = $('#st').val();
        var ed = $('#ed').val();
        if (st === "") st = null;
        if (ed === "") ed = null;
        if (st !== pre_st || ed !== pre_ed) {
            searchByDate(st, ed);
            pre_st = st;
            pre_ed = ed;
        }
    });

    var searchByDate = function (st, ed) {
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
                $.each(data['dates'], function (idx, info) {

                    var grade = info['userId'].substr(0, 4);
                    var userId = info['userId'] + ',' + info['userName'];

                    var acTimes = 0;
                    var subTimes = 0;

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

                $.each(grades, function (grade, info) {

                    var option_grade = $.extend(true, {}, option);

                    option_grade.title.text = option_grade.title.text + grade;

                    $.each(info, function (idx, x) {
                        option_grade.xAxis.data.push(x['userId']);
                        option_grade.series[0].data.push(x['acTimes']);
                        option_grade.series[1].data.push(x['subTimes']);
                    });

                    $("#chart").append("<div id = " + grade + " style=\"width: 100%;height:780px;margin:50px;\"></div>");
                    $("#chart").append("<div class=\"ui divider\"></div>");
                    var myChart = echarts.init($("#" + grade).get(0));
                    myChart.setOption(option_grade);
                });


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

});