// hallo fontfamily plugin
// (c) 2014 Alejandro Varas
// hallofontfamily may be freely distributed under the MIT license

(function(jQuery) {
  return jQuery.widget("IKS.ultracore-hallofontfamily", {
    options: {
      uuid: '',
      fonts: [
        // from http://web.mit.edu/jmorzins/www/fonts.html
	"Arial",
	"Helvetica",
        "Times New Roman",
	"Times",
        "Courier New",
        "Courier",
	// Other options that usually work cross-platform are:
        "Palatino",
        "Garamond",
        // "Bookman",
        // "Avant Garde",
	// Fonts that work on Windows and MacOS but not Unix+X are:
	"Verdana",
        "Georgia",
        "Comic Sans MS",
        "Trebuchet MS",
        "Arial Black",
        "Impact"
      ],
    },
    populateToolbar: function(toolbar) {
      var buttonset, widget,
      _this = this;
      widget = this;
      buttonset = jQuery("<span class=\"" + widget.widgetName + "\"></span>");
      this.createbuttons(buttonset);
      buttonset.hallobuttonset();
      toolbar.append(buttonset);
    },
    createbuttons: function (buttonset) {
      var _this = this
      jQuery.each(this.options.fonts, function(index) {
	var family = _this.options.fonts[index];
        var buttonElement;
        buttonElement = jQuery('<span></span>');
        buttonElement.hallobutton({
          uuid: _this.options.uuid,
          editable: _this.options.editable,
          label: family,
          command: 'fontName',
          commandValue: family,
          cssClass: _this.options.buttonCssClass,
        });
        buttonElement.find('.ui-button-text').css('font-family', family);
        buttonElement.find('.ui-button-text').text('F');
        buttonset.append(buttonElement);
      });
    },
  });
})(jQuery);
