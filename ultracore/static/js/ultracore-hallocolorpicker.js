// hallo colorpicker plugin
// (c) 2014 Alejandro Varas
// Based on https://github.com/25th-floor/hallo-simplecolorpicker-plugin
// hallocolorpicker may be freely distributed under the MIT license

(function(jQuery) {
  return jQuery.widget("IKS.ultracore-hallocolorpicker", {
    colorElement : null,
    options: {
      uuid: '',
      colors: {
        "#7bd148": "Green",
        "#5484ed": "Bold blue",
        "#a4bdfc": "Blue",
        "#46d6db": "Turquoise",
        "#7ae7bf": "Light green",
        "#51b749": "Bold green",
        "#fbd75b": "Yellow",
        "#ffb878": "Orange",
        "#ff887c": "Red",
        "#dc2127": "Bold red",
        "#dbadff": "Purple",
        "#e1e1e1": "Gray",
        "#000000": "Black"
      },
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
      jQuery.each(this.options.colors, function(color, label) {
        var buttonElement;
        buttonElement = jQuery('<span></span>');
        buttonElement.hallobutton({
          uuid: _this.options.uuid,
          editable: _this.options.editable,
          label: label,
          command: 'backColor',
          commandValue: color,
          cssClass: _this.options.buttonCssClass,
	  icon: 'fa fa-font'
        });
        buttonElement.find('.ui-button-text').css('background', color);
        buttonElement.find('.ui-button-text').text('C');
        buttonset.append(buttonElement);
      });
    },
  });
})(jQuery);
