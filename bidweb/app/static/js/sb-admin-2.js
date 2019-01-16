/*!
 * Start Bootstrap - SB Admin 2 v3.3.7+1 (http://startbootstrap.com/template-overviews/sb-admin-2)
 * Copyright 2013-2016 Start Bootstrap
 * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap/blob/gh-pages/LICENSE)
 */
$(function() {
    $('#side-menu').metisMenu();
});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        var topOffset = 50;
        var width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        var height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    // var element = $('ul.nav a').filter(function() {
    //     return this.href == url;
    // }).addClass('active').parent().parent().addClass('in').parent();
    var element = $('ul.nav a').filter(function() {
        return this.href == url;
    }).addClass('active').parent();

    while (true) {
        if (element.is('li')) {
            element = element.parent().addClass('in').parent();
        } else {
            break;
        }
    }
});


$(document).ready(function() {
    initDate();
    initRegion();
    initWebsite();
    initTables();
    bindEvents();
});


function initDate() {
    var endDate = new Date();
    $('#end_date').datepicker({
        autoclose: true,
        format: 'yyyy-mm-dd',
        todayBtn: true,
        todayHighlight: true,
        language: 'zh-CN'
    });
    $('#end_date').datepicker('setDate', endDate);

    var startDate = new Date(endDate.getTime() - 15 * 86400000);
    $('#start_date').datepicker({
        autoclose: true,
        format: 'yyyy-mm-dd',
        todayBtn: true,
        todayHighlight: true,
        language: 'zh-CN'
    });
    $('#start_date').datepicker('setDate', startDate);
}


// 同步执行
function initRegion() {
    $.ajax({
        url: '/json/regions',
        async: false,
        success: function(data) {
            //console.log(data);
            //console.log(data[0]);
            //console.log('initRegion');
            var html = template('region-art', {content: data.data});
            //console.log(html);

            $("#region").html(html);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.readyState);
        }
    })
}


// 同步执行
function initWebsite() {
    $.ajax({
        url: '/json/websites',
        async: false,
        success: function(data) {
            //console.log(data[0]);
            var html = template('website-art', {content: data.data});
            //console.log(data.data);
            //console.log(html);
            $("#website").html(html);
        }
    })
}

function initTables() {
    var params = {
        sdate: $('#start_date').val(),
        edate: $('#end_date').val(),
        region: $('#region').val(),
        website: $('#website').val(),
        word: $('#word').val()
    };

    $('#dataTables').DataTable({
        responsive: true,
        lengthChange: false,
        searching: false,
        serverSide: true,
        ordering: true,
        order: [3, 'desc'],
        pageLength: 12,
        language: {
            url: "/json/chinese"
        },
        ajax:{
            url: '/bids',
            type: 'POST',
            data: params
        },
        columns: [
            {'data': '_id'},
            {'data': '_source.title'},
            {'data': '_source.site'},
            {'data': '_source.pubdate'},
            {'data': '_source.region'},
            {'data': null}
        ],
        columnDefs: [
            {
                'targets': 0,
                'orderable': false
            },
            {
                'targets': 1,
                'searchable': false,
                'orderable': false,
                'render': function (data, type, row, meta) {
                    //console.log(data);
                    //console.log(type);
                    //console.log(row);
                    //console.log(meta);
                    return '<a target="_blank" href="' + row['_source']['url'] + '">' + data + '</a>';
                }
            },
            {
                'targets': 2,
                'orderable': false,
                'render': function(data, type, row, meta) {
                    //console.log(data);
                    return sites[data];
                }
            },
            {
                'targets': 3,
                'render': function(data, type, row, meta) {
                    console.log(data);
                    return data.substring(0, 10)
                }
            },
            {
                'targets': 4,
                'orderable': false,
                'render': function(data, type, row, meta) {
                    return regions[data];
                }
            },
            {
                'targets': -1,
                'searchable': false,
                'orderable': false,
                'render': function (data, type, row, meta) {
                    return '<button class="btn btn-primary btn-sm" data-toggle="modal" _id="' + row['_id'] + '">查看</button>';
                }
            }
        ]
    });
}


function bindEvents() {
    $('#dataTables').delegate('button[data-toggle]', 'click', function() {
        $('#detailModal').modal('show');
        $.ajax({
            url: '/bids/' + $(this).attr('_id'),
            success: function(data) {
                $('#detaiModalBody').html(data['_source']['details']);
            }
        });
    });

    //data-target=".bs-example-modal-lg"
    $('#search').click(function(){
        console.log('click');
        var params = {
            sdate: $('#start_date').val(),
            edate: $('#end_date').val(),
            region: $('#region').val(),
            website: $('#website').val(),
            word: $('#word').val()
        };

        var dataTables = $('#dataTables').DataTable();
        //console.log(dataTables.settings());
        dataTables.settings()[0].ajax.data = params;
        dataTables.ajax.reload();
    });
}

var regions = {
    '00': '全国',
    '01': '未分区域',

    '11': '北京市',
    '12': '天津市',
    '13': '河北省',
    '14': '山西省',
    '15': '内蒙古自治区',

    '21': '辽宁省',
    '22': '吉林省',
    '23': '黑龙江省',

    '31': '上海市',
    '32': '江苏省',
    '33': '浙江省',
    '34': '安徽省',
    '35': '福建省',
    '36': '江西省',
    '37': '山东省',

    '41': '河南省',
    '42': '湖北省',
    '43': '湖南省',
    '44': '广东省',
    '45': '广西壮族自治区',
    '46': '海南省',

    '50': '重庆市',
    '51': '四川省',
    '52': '贵州省',
    '53': '云南省',
    '54': '西藏自治区',

    '61': '陕西省',
    '62': '甘肃省',
    '63': '青海省',
    '64': '宁夏回族自治区',
    '65': '新疆维吾尔自治区',
};


var sites = {
    '000': '全部网站',

    '001': '中央政府采购网',
    '002': '中国招标网',
    '003': '千里马招标网',
    '004': '招标采购导航网',
    '005': '中国住建网',
    '006': '辽宁省政府采购网-中国采招网',

    '101': '北京市政府采购中心',
    '102': '天津市政府采购网',
    '103': '河北省政府采购网',
    '104': '河北省招标投标综合网',
    '105': '中国山西政府采购网',
    '106': '山西省省级政府采购中心',
    '107': '山西招投标网',
    '108': '内蒙古自治区',
    '109': '内蒙古自治区政府采购中心',

    '201': '辽宁政府采购网',
    '202': ' 辽宁省政府集中采购网',
    '203': '辽宁省政府采购-东北新闻网',
    '204': '吉林省政府采购中心',
    '205': '吉林省公共资源交易信息网',
    '206': '吉林市公共资源交易网',
    '207': '黑龙江省政府采购网',

    '301': '上海政府采购网',
    '302': '江苏政府采购网',
    '303': '南京市政府采购网',
    '304': '苏州市政府采购网',
    '305': '浙江政府采购网',
    '306': '安徽省政府采购网',
    '307': '安徽省招标投标信息网',
    '308': '福建省政府采购网',
    '309': '福建招标与采购网',
    '310': '江西省公共资源交易网',
    '311': '中国山东政府采购网',
    '312': '山东政府集中采购网',

    '401': '河南省政府采购网',
    '402': '湖北省政府采购网',
    '403': '湖南省政府采购网',
    '404': '湖南省公共资源交易中心政府集中采购操作系统',
    '405': '广东省政府采购网',
    '406': '广东省政府采购中心',
    '407': '广西壮族自治区政府采购网',
    '408': '中国海南政府采购网',

    '501': '重庆市政府采购网',
    '502': '四川省政府政务服务和公共资源交易服务中心',
    '503': '四川招投标网',
    '504': '四川政府采购',
    '505': '贵州省政府采购网',
    '506': '贵州省招标投标网',
    '507': '贵州省公共资源交易中心',
    '508': '云南省政府采购网',
    '509': '云南省公共资源交易中心',
    '510': '西藏自治区政府采购网',
    '511': '西藏自治区招标投标网',

    '601': '陕西省政府采购',
    '602': '甘肃政府采购网',
    '603': '青海省政府采购',
    '604': '宁夏政府采购公共服务平台',
    '605': '宁夏回族自治区公共资源交易网',
    '606': '新疆维吾尔自治区政府采购网'
};