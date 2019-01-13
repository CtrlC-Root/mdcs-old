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

  // ControlSet Detail view
  // ********************************
  var ControlSetDetailView = Backbone.View.extend({
    tagName: 'div',
    className: 'controlset',
    template: _.template($('#controlset-tmpl').html()),
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },
    render: function() {
      var html = this.template(this.model.toJSON());
      this.$el.html(html);

      return this;
    }
  });

  // ControlSet List view
  // ********************************
  var ControlSetListView = Backbone.View.extend({
    initialize: function() {
      this.listenTo(this.collection, 'update sync', this.render);
      this.collection.fetch();
    },
    render: function() {
      this.$el.empty();
      this.collection.each(function(model) {
        var item = new ControlSetDetailView({model: model});
        this.$el.append(item.render().$el);
      }, this);

      return this;
    }
  });

  // Application view
  // ********************************
  var RemoteView = Backbone.View.extend({
    el: $("#remote"),
    initialize: function() {
      // control sets
      this.controlSets = new ControlSetCollection();
      this.controlSetsList = new ControlSetListView({
        el: this.$('.controlsets'),
        collection: this.controlSets,
      });
    }
  });

  // Initialize application
  // ********************************
  var app = new RemoteView();

  // DEBUG
  // ********************************
  window.ControlSet = ControlSet;
  window.ControlSetCollection = ControlSetCollection;
});
