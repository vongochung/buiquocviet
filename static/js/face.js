      function logout(){
        FB.logout(function(response) {
            // Person is now logged out
            window.location.href= "/";
        });
      }

      function login(){
          FB.login(function(response) {
             if (response.status === 'connected') {
              FB.api('/me', function(response) {
                    window.location.href= "/facebook/"+response.id;
              });
              } else {
              window.location.href= "/";
              }
            }, {scope:'user_friends ,read_friendlists, public_profile, email'});
      }

      window.fbAsyncInit = function() {
          FB.init({
            appId      : '1504773003132119',//'1504773003132119',
            cookie     : true,  // enable cookies to allow the server to access 
                                // the session
            xfbml      : true,  // parse social plugins on this page
            version    : 'v2.2' // use version 2.1
          });

          /*FB.getLoginStatus(function(response) {
            statusChangeCallback(response);
          });*/

      };


      (function(d, s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "//connect.facebook.net/en_US/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
       }(document, 'script', 'facebook-jssdk'));