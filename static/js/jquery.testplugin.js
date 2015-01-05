(function($){
	$.fn.testPlugin = function(options){
		var defaults = {
			Text : "Test plugin",
			Color : "red"
		};

		var opt = $.extend({}, defaults, options);

		return this.each(function(){
			var $.ele = $(this);
			$.ele.css({
				"color": opt.Color,
			});

			$.ele.html(opt.Text);
			
		});
		
	};


})(jQuery);
/*$.widget( "myNamespace.testPlugin", {

    options: {
        // Default options
        Text : "Test plugin",
		Color : "red"
    },

    _create: function() {
        // Initialization logic here

    },

    // Create a public method.
    myPublicMethod: function( argument ) {
        // ...
    },

    // Create a private method.
    _myPrivateMethod: function( argument ) {
        // ...
    }

});*/