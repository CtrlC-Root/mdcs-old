// https://stackoverflow.com/questions/7348988/backbone-js-events-not-firing-after-re-render
// https://stackoverflow.com/questions/12028835/backbone-event-lost-in-re-render/12029250#12029250
// http://www.jquerybyexample.net/2012/05/empty-vs-remove-vs-detach-jquery.html
// https://www.joezimjs.com/javascript/backbone-js-subview-rendering-trick/

// Application code is loaded by jQuery once the DOM is ready.
$(function(){
  // Control Models
  // ********************************
  var Control = Backbone.Model.extend({
    urlRoot: function() {
      return new URL('control/', window.location.href).href;
    },
    idAttribute: 'uuid',
    defaults: {
      uuid: null,
      controlSetUuid: '',
      name: '',
      type: '',
      description: '',
      button: {
        title: ''
      },
      color: {},
    },
    parse: function(data, options) {
      var generic = {
        uuid: data.uuid,
        controlSetUuid: data.controlset_uuid,
        name: data.name,
        type: data.type.toLowerCase(),
        description: data.description,
      };

      switch (generic.type) {
        case 'button':
          return Object.assign(generic, {
            button: {
              title: data.button.title,
            }
          });

        case 'color':
          return Object.assign(generic, {color: {}});
      }

      console.warn('unknown control type: %s', generic.type);
      return generic;
    },
    toJSON: function() {
      var data = this.attributes;
      var generic = {
        uuid: data.uuid,
        controlset_uuid: data.controlSetUuid,
        name: data.name,
        type: data.type.toUpperCase(),
        description: data.description,
      };

      switch (data.type) {
        case 'button':
          return Object.assign(generic, {
            button: {
              title: data.button.title,
            }
          });

        case 'color':
          return Object.assign(generic, {color: {}});
      }

      console.warn('unknown control type: %s', generic.type);
      return generic;
    },
  });

  // Control Collection
  // ********************************
  var ControlCollection = Backbone.Collection.extend({
    model: Control,
    url: function() {
      return new URL('control/', window.location.href).href;
    },
    initialize: function(models, options) {
      this.controlSet = null;
      if (options !== undefined) {
        if ('controlSet' in options) {
          this.controlSet = options.controlSet;
        }
      }
    },
    parse: function(data) {
      var controls = Backbone.Collection.prototype.parse.apply(this, arguments);
      if (this.controlSet == null) {
        return controls;
      }

      return controls.filter(control => control.controlset_uuid == this.controlSet.attributes.uuid);
    },
  });

  // ControlSet Model
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
      'click a[data-action=delete]': 'onDelete'
    },
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },
    render: function() {
      this.$el.html(this.template({
        'vid': this.cid,
        'model': this.model.attributes
      }));

      return this;
    },
    onDelete: function(event) {
      event.preventDefault();
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
      this.$el.html(this.template({'vid': this.cid}));
      var $tbody = this.$('tbody');

      $tbody.empty();
      this.collection.each(function(model) {
        var item = new ControlSetRowView({model: model});
        $tbody.append(item.render().$el);
      }, this);

      return this;
    }
  });

  // Application views
  // ********************************
  var DashboardView = Backbone.View.extend({
    template: _.template($('#remote-dashboard-tmpl').html()),
    events: {
      'click input[data-action=create]': 'onCreate'
    },
    initialize: function() {
      this.controlSets = new ControlSetCollection();
      this.render();
    },
    render: function() {
      this.$el.html(this.template({'vid': this.cid}));
      new ControlSetTableView({
        el: this.$(`#${this.cid}-controlsets`),
        collection: this.controlSets
      });

      return this;
    },
    onCreate: function(event) {
      // don't submit the form
      event.preventDefault();

      // retrieve form values
      var $name = this.$(`#${this.cid}-name`);
      var $configType = this.$(`#${this.cid}-configType`);
      var $description = this.$(`#${this.cid}-description`);

      // TODO: validation

      // create the new control set
      this.controlSets.create({
        name: $name.val(),
        configType: $configType.val(),
        description: $description.val()
      });

      // reset the form
      this.$('input[data-action=reset]').click();
    }
  });

  var ControlSetView = Backbone.View.extend({
    template: _.template($('#remote-controlset-tmpl').html()),
    buttonTemplate: _.template($('#remote-controlcard-button-tmpl').html()),
    colorTemplate: _.template($('#remote-controlcard-color-tmpl').html()),
    events: {
      'click button[data-action=save]':    'onSave',
      'click button[data-action=refresh]': 'onRefresh'
    },
    initialize: function() {
      this.controls = new ControlCollection(null, {controlSet: this.model});

      // XXX: this results in multiple calls to this.render() but
      // ideally there would only be one

      this.listenTo(this.model, 'sync change', this.render);
      this.listenTo(this.controls, 'sync update', this.render);

      this.model.fetch();
      this.controls.fetch();
    },
    render: function() {
      this.$el.html(this.template({
        'vid': this.cid,
        'model': this.model.attributes
      }));

      var cards = this.controls.map(function(control) {
        switch (control.get('type')) {
          case 'button':
            return $(this.buttonTemplate({
              'vid': this.cid,
              'model': control.attributes
            }));

          case 'color':
            return $(this.colorTemplate({
              'vid': this.cid,
              'model': control.attributes
            }));
        }
      }, this);

      // TODO: add the placeholder card for creating a new control

      var controls = this.$(`#${this.cid}-controls`);
      controls.empty();

      while (cards.length > 0) {
        var row = controls.find('div.row').last();
        if (row.length == 0) {
          row = $('<div/>', {class: 'row'});
          controls.append(row);
        }

        var column = $('<div/>', {class: 'four columns'});
        column.append(cards.shift());
        column.appendTo(row);
      }

      return this;
    },
    onSave: function() {
      // TODO: validation
      this.model.save({
        name: this.$(`#${this.cid}-name`).val(),
        configType: this.$(`#${this.cid}-configType`).val(),
        description: this.$(`#${this.cid}-description`).val(),
        config: this.$(`#${this.cid}-config`).val(),
      });
    },
    onRefresh: function() {
      this.model.fetch();
    }
  });

  // Application router
  // ********************************
  var RemoteRouter = Backbone.Router.extend({
    routes: {
      'dashboard':        'showDashboard',
      'controlset/:uuid': 'showControlSet',

      '*path':            'showDashboard'
    },
    activeView: null,
    removeActiveView: function() {
      if (this.activeView != null) {
        this.activeView.undelegateEvents();
      }

      this.activeView = null;
    },
    showDashboard: function() {
      this.removeActiveView();
      this.activeView = new DashboardView({
        el: $('#remote')
      });
    },
    showControlSet: function(uuid) {
      this.removeActiveView();
      this.activeView = new ControlSetView({
        el: $('#remote'),
        model: new ControlSet({uuid: uuid})
      });
    }
  });

  // Initialize application
  // ********************************
  var router = new RemoteRouter();
  Backbone.history.start();

  // DEBUG
  // ********************************
  window.Control = Control;
  window.ControlCollection = ControlCollection;
  window.ControlSet = ControlSet;
  window.ControlSetCollection = ControlSetCollection;
});
