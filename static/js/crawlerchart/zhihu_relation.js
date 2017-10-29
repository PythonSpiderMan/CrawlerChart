function relation(title, title_text, series_data, series_links, series_categories) {
    var myChart = echarts.init(document.getElementById('relation'));
    var option = {
        backgroundColor: new echarts.graphic.RadialGradient(0.3, 0.3, 0.8, [{
            offset: 0,
            color: '#f7f8fa'
        }, {
            offset: 1,
            color: '#cdd0d5'
        }]),
        title: title,
        tooltip: {},
        legend: [{
            formatter: function (name) {
                return echarts.format.truncateText(name, 60, '18px Microsoft Yahei', '…');
            },
            tooltip: {
                show: true
            },
            selectedMode: 'false',
            bottom: 20,
            // 分支数据汇总, 是下面的分类
            data: [title_text]
        }],
        toolbox: {
            show: true,
            feature: {
                dataView: {show: true, readOnly: true},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        animationDuration: 3000,
        animationEasingUpdate: 'quinticInOut',
        series: [{
            name: title.text,
            type: 'graph',
            layout: 'force',

            force: {
                repulsion: 50
            },
            // 定义分支结构的值
            data: series_data,

            // 定义关系, 分支属于谁
            links: series_links,
            categories: series_categories,
            focusNodeAdjacency: true,
            roam: true,
            label: {
                normal: {
                    show: true,
                    position: 'top'
                }
            },
            lineStyle: {
                normal: {
                    color: 'source',
                    curveness: 0,
                    type: "solid"
                }
            }
        }]
    };
    myChart.setOption(option);
}

// 得到查询字符串
function param() {
    query = window.location.search.substring(1);
    return query.split('=')[1];
}

$(function () {
    query_string = param();
    $.post("/api/v1/search", {
            'url_token': param()
        },
        function (result) {
            if (result.status == 1) {
                title_text = result.data.series_data[0].name;
                title = {
                    text: title_text,    // 标题
                    subtext: query_string,  // 子标题
                    top: "top",
                    left: "center"
                };
                relation(title, title_text, result.data.series_data, result.data.series_links, result.data.series_categories)
            }
        }
    );
});