$(function() {            
    loading($("#relative-post"));
    var url = "/relative-post/{{ post.category.slug }}/";
    setTimeout(function () {
        $.ajax({
            url: url,
            type: "GET",
            data:{"post":"{{ post.id }}"},
            dataType: 'json',  
            success: function (result) {
                loading($("#relative-post"));
                $("#relative-post").append(result.html);
                displayPlayer();
                $('[data-toggle="popover"]').popover({trigger: 'hover','placement': 'top'});
            },
            complete: function () {
                console.log("xong");
            }
        });
    }, 3000);
});
window.fbAsyncInit = function() {
    FB.init({
        appId      : '1504773003132119',
        cookie     : true,  // enable cookies to allow the server to access 
                            // the session
        xfbml      : true,  // parse social plugins on this page
        version    : 'v2.2' // use version 2.1
    });

    // In your onload method
    FB.Event.subscribe('comment.create', comment_create);
    FB.Event.subscribe('comment.remove', comment_remove);
    FB.Event.subscribe('edge.create', edge_create);
    FB.Event.subscribe('edge.remove', edge_remove);
};
function comment_create(response) {
    $.ajax({
        url: '/commented/',
        type: 'POST',
        data: {"p":"{{post.id}}"},
    })
    .done(function(data) {    
        console.log("commented");         
    })
    .fail(function() {
        console.log("error comment");
    })
    .always(function() {
    });
}
function comment_remove(response) {
    $.ajax({
        url: '/commented/',
        type: 'POST',
        data: {"p":"{{post.id}}", "type":"removed"},
    })
    .done(function(data) {    
        console.log("removed");         
    })
    .fail(function() {
        console.log("error comment");
    })
    .always(function() {
    });
}
function edge_create(response) {
    $.ajax({
        url: '/liked/',
        type: 'POST',
        data: {"p":"{{post.id}}"},
    })
    .done(function(data) {    
        console.log("liked");         
    })
    .fail(function() {
        console.log("error liked");
    })
    .always(function() {
    });
}
function edge_remove(response) {
    $.ajax({
        url: '/liked/',
        type: 'POST',
        data: {"p":"{{post.id}}", "type":"unliked"},
    })
    .done(function(data) {    
        console.log("unliked");         
    })
    .fail(function() {
        console.log("error unliked");
    })
    .always(function() {
    });
}