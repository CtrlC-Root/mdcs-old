import Vue from 'vue'

const state = {
  all: []
};

const getters = {
  lastNode: function (state) {
    if (state.all.length == 0) {
      // XXX better way to handle this?
      return null;
    }

    return state.all[state.all.length - 1];
  }
};

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
    var nodeUrl = new URL(params.nodeUrl);
    Vue.http.get(params.nodeUrl).then((response) => {
      // success
      return response.json();
    }, (response) => {
      // TODO error
      console.log(response);
      return {};
    }).then((data) => {
      context.commit('addNode', {
        name: data.name,
        loading: true,
        host: nodeUrl.hostname,
        httpPort: data.config.httpPort,
        tcpPort: data.config.tcpPort
      });

      context.dispatch('refreshNode', context.getters.lastNode);
    });
  },

  refreshNode: function (context, node) {
    context.commit('updateNode', {name: node.name, loading: true});
    Vue.http.get(`http://${node.host}:${node.httpPort}/devices`).then((response) => {
      // success
      return response.json();
    }, (response) => {
      // TODO error
      return [];
    }).then((data) => {
      context.commit('updateNode', {
        name: node.name,
        loading: false,
        devices: data.devices
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
