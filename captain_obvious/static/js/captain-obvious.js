var uids = new Array();

function collectUids() {
    var comments = $("[class^=comment-]");
    for(var idx in comments) {
        if(isNaN(parseInt(idx)))
            continue;
        var comment = $(comments[idx]);
        var className = comment.attr('class');
        var tokens = className.split('-');
        var uid = tokens[1];
        if($.inArray(uid, uids) == -1)
            uids.push(uid);
    }
}

function fillUids() {
    for(var idx in uids) {
        $.get('/graph/user', {uid: uids[idx]}, function(res) {
            $('.profile-' + res.uid).attr('src', res.profile);
            $('.name-' + res.uid).html(res.name);
        }, 'json');
    }
}

function makeGoogleLink(keywords) {
    return 'https://www.google.com.tw/search?hl=zh-TW&safe=off&biw=1366&bih=682&site=imghp&tbm=isch&source=hp&biw=1366&bih=682&q=' + keywords + '&oq=meme+i+dont+always&gs_l=img.3...3278.3278.0.3809.1.1.0.0.0.0.76.76.1.1.0...0.0...1ac..4.img.q58sBgJwKbo';
}

function findMemeClass() {
    $.get('/mc', {gag_id: $('#gag-id').val()}, function(res) {
        if(res.meme_class == null)
            $('.meme-class').html('not a meme : (');
        else {
            var memeLink = $('<a></a>');
            memeLink.html(res.meme_class);
            memeLink.attr('href', makeGoogleLink(res.meme_class));
            memeLink.attr('target', '_blank');
            $('.meme-class').html(memeLink);
        }
    }, 'json');
}

function fillGag() {
    $.get('/9gag/post', {gag_id: $('#gag-id').val()}, function(res) {
        $('#gag-title').html(res.gag_title);
        $('#gag-img').attr('src', res.gag_img_url);
        $('#gag-img').attr('class', 'img-polaroid');
    }, 'json');
}

function fillComments() {
    $.get('/graph/comments', {gag_id: $('#gag-id').val()}, function(res) {
        var table = $('#gag-comments');
        for(var idx in res.comments) {
            var comment = res.comments[idx];
            var tr = $('<tr></tr>');
            tr.attr('class', 'comment-' + comment.uid);
            var imgProfile = $('<img></img>').attr('src', '/static/img/yao-ming.jpg')
                                             .attr('class', 'profile-' + comment.uid);
            var tdProfile = $('<td></td>').attr('width', '60').append(imgProfile);
            var tdContent = $('<td></td>').append($('<p></p>').attr('class', 'name-' + comment.uid).html('Somebody'))
                                          .append($('<p></p>').html(comment.content));
            if(comment.is_lead)
                tdContent.attr('colspan', '2');
            else
                tr.append($('<td></td>'));
            tr.append(tdProfile);
            tr.append(tdContent);
            table.append(tr);
        }
        collectUids();
        fillUids();
    }, 'json');
}

$(function() {
    findMemeClass();
    fillGag();
    fillComments();
});

