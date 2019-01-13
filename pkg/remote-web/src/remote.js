// Application code is loaded by jQuery once the DOM is ready.
$(function(){
  // ControlSet Model (ESksfnYfHPrPc5Rb5Cdfgk)
  // ********************************
  var ControlSet = Backbone.Model.extend({
    urlRoot: function() {
      return new URL('controlset/', window.location.href).href;
    },
    idAttribute: 'uuid',
    defaults: {
      uuid: null,
      name: '',
      description: '',
      configType: 'lua',
      config: '-- nothing',
    },
    parse: function(data, options) {
      return {
        uuid: data.uuid,
        name: data.name,
        description: data.description,
        configType: data.config_type.toLowerCase(),
        config: data.config,
      };
    },
    toJSON: function() {
      var data = this.attributes;
      return {
        uuid: data.uuid,
        name: data.name,
        description: data.description,
        config_type: data.configType.toUpperCase(),
        config: data.config,
      };
    },
  });

  // ControlSet Collection
  // ********************************
  var ControlSetCollection = Backbone.Collection.extend({
    model: ControlSet,
    url: function() {
      return new URL('controlset/', window.location.href).href;
    },
  });

  // Application view
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
