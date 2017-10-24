function top10(yAxis_data, series_data) {
    var myChart = echarts.init(document.getElementById('top10'));
    var option = {
    title: {
        text: '知乎用户粉丝排名'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['粉丝']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'value',
        boundaryGap: [0, 0.01]
    },
    yAxis: {
        type: 'category',
        data: yAxis_data
    },
    series: [
        {
            name: '粉丝',
            type: 'bar',
            data: series_data
        }
        ]
    };
    myChart.setOption(option);
}


$(document).ready(function () {
    // 发起请求
    $.get('/api/v1/top10', function (result) {
        var yAxis_data = new Array();
        var series_data = new Array();
        if (result.status==1){
            user = result.data;
            user_legnth = user.length;
            for (var i=0; i<user_legnth; i++){
                yAxis_data[i] = user[i].name;
                series_data[i] = user[i].follower_count;
            }
        }
        top10(yAxis_data.reverse(), series_data.reverse())
    });
});




