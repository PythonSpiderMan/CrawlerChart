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
        data: ['巴西','印尼','美国','印度','中国','世界人口(万)']
    },
    series: [
        {
            name: '粉丝',
            type: 'bar',
            data: [18203, 23489, 29034, 104970, 131744, 630230]
        }
        ]
    };
    myChart.setOption(option);
}


$(document).ready(function () {
    // 发起请求
    $.get('/api/v1', function (data) {
        alert(data)
    });
    top10('d', 'd')
});




