$(function() {
    $(window).on("scroll", get_more_post);
    $(window).on("resize", displayPlayer);
    displayPlayer();
    set_category();
    init_search();
});

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});

function set_category(){
    h = $(window).height();
    if (h < 480){
        //$("#category").css({"max-height": h-20, "overflow-y":"scroll"});
    }
   
}
function displayPlayer() {
    $(".player").each(function(){
        var player = $(this),
        $link = player.next(),
        offset = player.position(),
        w = player.width(),
        h = player.innerHeight(),
        t = offset.top,
        l = offset.left;
        $link.css({left: l+w/2-$link.width()/2, top: t+h/2-$link.height()/2});
    });
    set_category();
    
}

function loading(btn)
{
    var loading = btn.find('.loading').length
    if (loading) {
        btn.find('.loading').remove()
    } else {
        btn
            .html('<i class="fa fa-spinner fa-spin loading"></i>' + btn.html()).addClass("text-center")
    }
}

function toogleMenu(){
   $('#category').toggleClass('hides');
   if ($('#category').hasClass('hides')) {
        $('#btn-pullout').animate({left:242});
        $('#category').offset({top:$('#btn-pullout').offset().top});
        $('#category').animate({left:0});
   } else{
        $('#category').animate({left: -242});
        $('#btn-pullout').animate({left:0});
   }
}


function get_more_post(){
    var scrollAmount = $(window).scrollTop(),
    documentHeight = $(document).height(),
    content = $(window).height();
    if(scrollAmount == (documentHeight - content)) {
        $(".viewmore-post").click();
        $(".viewmore-category").click();
    }
}

$(document).on("click",".viewmore-post",function(e) {
    var $ele = $(this);
    loading($ele)
    var page = $(this).data("page"),
    category = $(this).data("category");
    var data = {
        "page": page
    }
    if ( typeof category !== "undefined"){
        data["category"] = category;
    }
    $.ajax({
        url: '/get-posts/',
        type: 'POST',
        data: data,
    })
    .done(function(data) {    
        $("#post-wrap").append(data.html);            
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        $ele.parent().remove();
        displayPlayer();
        try{
            FB.XFBML.parse(); 
        }catch(ex){
            console.log(ex);
        }
    });
        
});

$(document).on("click",".viewmore-post-detail",function(e) {
    var $ele = $(this);
    loading($ele)
    var page = $(this).data("page"),
    typeGet = $(this).data("type"),
    category = $(this).data("category");
    var data = {
        "page": page,
        "type":typeGet
    }
    if ( typeof category !== "undefined"){
        data["category"] = category;
    }
    $.ajax({
        url: '/get-posts-detail-more/',
        type: 'POST',
        data: data,
    })
    .done(function(data) {    
        $("#"+typeGet).append(data.html);
        $('[data-toggle="popover"]').popover({trigger: 'hover','placement': 'top'});            
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        $ele.parent().remove();
        displayPlayer();
    });
        
});

$(document).on("click",".active-language",function(e) {
    $("#set-lang").val($(this).data("lang"));
    $("#form-language").submit();
});

$(document).on("click",".viewmore-category",function(e) {
    var $ele = $(this);
    loading($ele);
    call_loading();
    var page = $(this).data("page"),
    data = {
        "page": page
    };
    $ele.parent().remove();
    $.ajax({
        url: '/get-categories/',
        type: 'POST',
        data: data,
    })
    .done(function(data) {    
        $("#post-wrap").append(data.html);            
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        $ele.parent().remove();
        call_loading();
    });
        
});

var cache = {};

this.tmpl = function tmpl(str, data){
// Figure out if we're getting a template, or if we need to
// load the template - and be sure to cache the result.
var fn = !/\W/.test(str) ?
  cache[str] = cache[str] ||
    tmpl(document.getElementById(str).innerHTML) :
 
  // Generate a reusable function that will serve as a template
  // generator (and which will be cached).
  new Function("obj",
    "var p=[],print=function(){p.push.apply(p,arguments);};" +
   
    // Introduce the data as local variables using with(){}
    "with(obj){p.push('" +
   
    // Convert the template into pure JavaScript
    str
      .replace(/[\r\t\n]/g, " ")
      .split("<%").join("\t")
      .replace(/((^|%>)[^\t]*)'/g, "$1\r")
      .replace(/\t=(.*?)%>/g, "',$1,'")
      .split("\t").join("');")
      .split("%>").join("p.push('")
      .split("\r").join("\\'")
  + "');}return p.join('');");

// Provide some basic currying to the user
return data ? fn( data ) : fn;
};

$(document).on("click","#btn-tim",function(e) {
    call_loading();
    $("#post-wrap").html("");
    $(".next-post").remove();
    $.each(data_search, function(index, val) {
        var html =  tmpl("item_tmpl", {
            name: val.value,
            url : val.url,
            image: val.image
        });
        $("#post-wrap").append(html); 
    });
    call_loading();
});


function call_loading(){
    $("#ele-loading").toggleClass("hide");
}

/* -------------- instant search in dashboard --*/
data_search = []
function init_search()
{
    var input = $("#txt-search");

    if (! input.length) {
        return;
    }

    input.autocomplete({
      source: function( request, response ) {
        $.ajax({
          url:"/intance-search/",//
          dataType: "jsonp",
          data: {
            q: request.term
          },
          success: function( data ) {
            data_search = $.map(data, function(item) {
                return {
                    label: item.name,
                    value: item.name,
                    image: item.image,
                    url: item.url,
                };
            })
            response(data_search);
          }
        });
      },
      minLength: 3,
      select: function( event, ui ) {
        document.location.href=ui.item.url;
      },
      open: function() {
        $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
      },
      close: function() {
        $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
      }
    }).autocomplete( "instance" )._renderItem = function( ul, item ) {
      return $( "<li>" )
        .append( '<a href="'+ item.url +'"><img class="profile-img medium" src="'+ item.image +'"><span class="name-search">' + item.label + "</span></a>" )
        .appendTo( ul );
    };

}