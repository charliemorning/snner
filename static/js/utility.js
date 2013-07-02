/**
 * Created with PyCharm.
 * User: charlie
 * Date: 6/5/13
 * Time: 9:53 PM
 * To change this template use File | Settings | File Templates.
 */


var _getCookie = function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function getStatusesPagedHTML(param, div) {
    $.ajax({
        url : '/network/status/show',
        data : param,
        dataType : 'html',
        type : 'GET',
        cache: false,
        async : true,
        success : function(result) {
            $('#' + div).html(result);
        },
        error : function() {
            alert('error');
        }
    })
}

function statusGotoPage(uid, page, div) {

    var param = {
        page : page,
        uid : uid
    };

    debugger

    getStatusesPagedHTML(param, div);

}


function getStatusesPagedByKeyword(page, keyword, div) {

    var param = {
        page : page,
        keyword : keyword,
        exclude : '1987543647'
    };

    getStatusesPagedHTML(param, div);

}





function recognizeByIDs(idsStr, sns) {

    $.ajax({
        url : '/ner/recognize',
        data : {
            ids : idsStr,
            sns : sns
        },
        dataType : 'json',
        type : 'get',
        cache: false,
        async : true,
        headers: {
            "X-CSRFToken" : _getCookie('csrftoken')
        },
        success : function(result) {

            if (results.status == 'ok') {
                console.log(results.msg);
            }

        },
        error : function() {
            alert('error');
        }
    })

}


var recognizeByIDRange = function(uid, gte) {
    $.ajax({
        url : '/ner/recognize',
        data : {
            uid : uid,
            gte : gte
        },
        dataType : 'json',
        type : 'get',
        cache: false,
        async : true,
        headers: {
            "X-CSRFToken" : _getCookie('csrftoken')
        },
        success : function(result) {

            if (results.status == 'ok') {
                console.log(results.msg);
            }

        },
        error : function() {
            alert('error');
        }
    })

};