function relation() {
    var myChart = echarts.init(document.getElementById('relation'));
    var option = {
        backgroundColor: new echarts.graphic.RadialGradient(0.3, 0.3, 0.8, [{
            offset: 0,
            color: '#f7f8fa'
        }, {
            offset: 1,
            color: '#cdd0d5'
        }]),
        title: {    // 从series_data中获取
            text: "关系图谱",
            subtext: "公司关系",
            top: "top",
            left: "center"
        },
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
            data: ['计算机科学与教育软件学院', '地理科学学院', '机械与电气工程学院']
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
            name: '广州大学',    // 从series获取
            type: 'graph',
            layout: 'force',

            force: {
                repulsion: 50
            },
            // 定义分支结构的值
            data: [{
                "name": "广州大学",    // 中心数据
                // "x": 0,
                // y: 0,
                "symbolSize": 20,    // 球形大小
                "draggable": "true",
                "value": 27          // 数值

            }, {
                "name": "计算机科学与教育软件学院",
                "value": 1,
                "symbolSize": 20,
                "category": "计算机科学与教育软件学院",    // 和name保持一致
                "draggable": "true"
            }, {
                "name": "地理科学学院",
                "value": 1,
                "symbolSize": 18,
                "category": "地理科学学院",
                "draggable": "true"
            }, {
                "name": "机械与电气工程学院",
                "value": 1,
                "symbolSize": 15,
                "category": "机械与电气工程学院",
                "draggable": "true"
            }],

            // 定义关系, 分支属于谁
            links: [{
                "source": "广州大学",
                "target": "计算机科学与教育软件学院"
            }, {
                "source": "广州大学",
                "target": "地理科学学院"
            }, {
                "source": "广州大学",
                "target": "机械与电气工程学院"
            }],
            categories: [{
                'name': '计算机科学与教育软件学院'
            }, {
                'name': '地理科学学院'
            }, {
                'name': '机械与电气工程学院'
            }],
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

$(function () {
    relation()
});