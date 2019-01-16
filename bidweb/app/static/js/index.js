/**
 * Created by block on 11/3/17.
 */

console.log('index.js');
regions = {
    '0': 'quanguo',
    '1': 'beijing'
};

template.defaults.imports.regionMap = function(reg) {
  return regions[reg];
};

$(document).ready(function() {
    renderTable();
    renderPage(20, 5, 11);

});


function renderTable2() {
    var $table = $("table");
    $table.bootstrapTable();
}


function renderTable() {
    var data = [
        {
            id: 12, title: '东坝农林基地综合整治电力增容及供电线路改造项目设计招标公告', name: '中央政府采购网', region: 0,
            url: 'http://www.zycg.gov.cn/article/show/483393', pubdate: '2017-11-02T00:00:00'
        },
        {
            id: 12, title: '东坝农林基地综合整治电力增容及供电线路改造项目设计招标公告', name: '中央政府采购网', region: 0,
            url: 'http://www.zycg.gov.cn/article/show/483393', pubdate: '2017-11-02T00:00:00'
        }
    ];
    var html = template('table-content-art', {content: data});
    $("#table-content").html(html);
}




function renderPage(count, visible_pages, current_page) {
}