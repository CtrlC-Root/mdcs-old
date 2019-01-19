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

  // ControlSet Detail views
  // ********************************
  var ControlSetRowView = Backbone.View.extend({
    tagName: 'tr',
    template: _.template($('#remote-cs-row-tmpl').html()),
    events: {
      'click button.controlset-delete': 'onDelete'
    },
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },
    render: function() {
      this.$el.html(this.template(this.model.attributes));
      return this;
    },
    onDelete: function() {
      this.model.destroy();
    }
  });

  // ControlSet List views
  // ********************************
  var ControlSetTableView = Backbone.View.extend({
    template: _.template($('#remote-cs-table-tmpl').html()),
    initialize: function() {
      this.listenTo(this.collection, 'update sync', this.render);
      this.collection.fetch();
    },
    render: function() {
      this.$el.html(this.template());
      var $tbody = this.$('tbody');

      $tbody.empty();
      this.collection.each(function(model) {
        var item = new ControlSetRowView({model: model});
        $tbody.append(item.render().$el);
      }, this);

      return this;
    }
  });

  // Application view
  // ********************************
  var RemoteView = Backbone.View.extend({
    el: $("#remote"),
    events: {
      'click #controlset-create': 'onCreate'
    },
    initialize: function() {
      // control sets
      this.controlSets = new ControlSetCollection();
      this.controlSetsList = new ControlSetTableView({
        el: this.$('.remote-controlsets'),
        collection: this.controlSets,
      });
    },
    onCreate: function(event) {
      // don't submit the form
      event.preventDefault();

      // retrieve form values
      var $name = this.$('#controlset-name');
      var $configType = this.$('#controlset-configType');
      var $description = this.$('#controlset-description');

      // TODO: validation

      // create the new control set
      this.controlSets.create({
        name: $name.val(),
        configType: $configType.val(),
        description: $description.val()
      });

      // reset the form
      this.$('#controlset-reset').click();
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
