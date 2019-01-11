// Application code is loaded by jQuery once the DOM is ready.
$(function(){
  // ControlSet Model (ESksfnYfHPrPc5Rb5Cdfgk)
  // ********************************
  var ControlSet = Backbone.Model.extend({
    urlRoot: '/controlset/',
    idAttribute: 'uuid',
    defaults: {
      uuid: '',
      name: '',
      description: '',
      configType: '',
    },
    parse: function(data, options) {
      return {
        uuid: data.uuid,
        name: data.name,
        description: data.description,
        configType: data.config_type.toLowerCase(),
      };
    },
    toJSON: function() {
      var data = this.attributes;
      return {
        uuid: data.uuid,
        name: data.name,
        description: data.description,
        config_type: data.configType.toUpperCase(),
      };
    },
  });

  // ControlSet Collection
  // ********************************
  var ControlSetCollection = Backbone.Collection.extend({
    url: '/controlset/',
    model: ControlSet,
  });

  // Application
  // ********************************
  var RemoteView = Backbone.View.extend({
    el: $("#remote"),
    initialize: function() {
      // TODO
    },
    render: function() {
      // TODO
    }
  });

  // TODO
  // ********************************
  var app = new RemoteView();

  // DEBUG
  // ********************************
  window.ControlSet = ControlSet;
  window.ControlSetCollection = ControlSetCollection;
});
