// jquery-simplecolorpicker plugin for Hallo
// (c) 2013 Thomas Subera, 25th-Floor
// Hallo may be freely distributed under the MIT license
(function(jQuery) {
  return jQuery.widget("IKS.ultracore-hallofontsize", {
    colorElement : null,
    options: {
      uuid: '',
    },
    editable: null,

    populateToolbar: function(toolbar) {
      var buttonize, buttonset, _this = this;
      buttonset = jQuery("<span class=\"" + this.widgetName + "\"></span>");
      buttonize = function(alignment, command, size) {
        var buttonElement;
        buttonElement = jQuery('<span></span>');
        buttonElement.hallobutton({
          uuid: _this.options.uuid,
          editable: _this.options.editable,
          label: alignment,
          command: command,
          commandValue: size,
          cssClass: _this.options.buttonCssClass
        });
	// overrides button font
	buttonElement.find('.ui-button-text').text(size + '');
        return buttonset.append(buttonElement);
      };
      buttonize("Font 1", "fontSize", 1);
      buttonize("Font 2", "fontSize", 2);
      buttonize("Font 3", "fontSize", 3);
      buttonize("Font 4", "fontSize", 4);
      buttonize("Font 5", "fontSize", 5);
      buttonize("Font 6", "fontSize", 6);
      buttonize("Font 7", "fontSize", 7);
      buttonset.hallobuttonset();
      return toolbar.append(buttonset);
    }
  });
})(jQuery);
