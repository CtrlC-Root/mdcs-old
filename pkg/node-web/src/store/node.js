import Vue from 'vue';

const state = {
  all: []
};

const getters = {
  lastNode: function (state) {
    // corner case: no last node
    if (state.all.length == 0) {
      return null;
    }

    // return last node added to the list
    return state.all[state.all.length - 1];
  }
};

function parseDevice(device) {
  var attributes = device.attributes.map(function (attribute) {
    return {
      path: attribute.path,
      flags: attribute.flags,
      schema: JSON.parse(attribute.schema),
    };
  });

  var actions = device.actions.map(function (action) {
    return {
      path: action.path,
      inputSchema: JSON.parse(action.input_schema),
      outputSchema: JSON.parse(action.output_schema),
    };
  });

  return {
    name: device.name,
    attributes: attributes,
    actions: actions,
  };
}

const mutations = {
  addNode: function (state, node) {
    // TODO: verify node.name exists and is unique
    state.all.push(Object.assign({
      loading: false,
      name: '',
      host: '',
      httpPort: NaN,
      tcpPort: NaN,
      devices: [],
    }, node));
  },

  updateNode: function (state, node) {
    // TODO: is there a more efficient way given Vue's reactivity constraints?
    // https://vuejs.org/v2/guide/reactivity.html
    var index = state.all.findIndex(function (item) {
      return item.name == node.name;
    });

    var existing = state.all[index];
    state.all.splice(index, 1);
    state.all.push(Object.assign({}, existing, node));
  },

  removeNode: function (state, node) {
    state.all = state.all.filter(function (item) {
      return item.name != node.name;
    });
  }
};

const actions = {
  connectNode: function (context, params) {
    // retrieve node configuration
    return Vue.http.get(params.nodeUrl).then((response) => {
      return response.json();
    }).then((data) => {
      // create initial node object
      var parsedUrl = new URL(params.nodeUrl);
      return {
        name: data.name,
        host: parsedUrl.hostname,
        httpPort: data.config.http_port,
        tcpPort: data.config.tcp_port
      };
    }).then((node) => {
      // retrieve node devices
      return Vue.http.get(`http://${node.host}:${node.httpPort}/d`).then((response) => {
        return response.json();
      }).then((data) => {
        return Object.assign(node, {
          devices: data.map(parseDevice)
        });
      });
    }).then((node) => {
      context.commit('addNode', node);
      return node;
    });
  },

  refreshNode: function (context, node) {
    context.commit('updateNode', {name: node.name, loading: true});
    return Vue.http.get(`http://${node.host}:${node.httpPort}/d`).then((response) => {
      return response.json();
    }).then((data) => {
      context.commit('updateNode', {
        name: node.name,
        loading: false,
        devices: data.map(parseDevice)
      });
    });
  }
};

export default {
  state: state,
  getters: getters,
  mutations: mutations,
  actions: actions
};
