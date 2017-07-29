import Vue from 'vue'

const state = {
  nextId: 0,
  all: []
};

const mutations = {
  addNode: function (state, node) {
    state.all.push(Object.assign({
      id: state.nextId,
      loading: false,
      host: '',
      httpPort: NaN,
      tcpPort: NaN,
      devices: []
    }, node));

    state.nextId++;
  },

  updateNode: function (state, node) {
    // TODO: is there a more efficient way given Vue's reactivity constraints?
    // https://vuejs.org/v2/guide/reactivity.html
    var index = state.all.findIndex(function (item) {
      return item.id == node.id;
    });

    var existing = state.all[index];
    state.all.splice(index, 1);
    state.all.push(Object.assign({}, existing, node));
  },

  removeNode: function (state, node) {
    state.all = state.all.filter(function (item) {
      return item.id != node.id;
    });
  }
};

const actions = {
  refreshNode: function (context, node) {
    context.commit('updateNode', {id: node.id, loading: true});
    Vue.http.get(`http://${node.host}:${node.httpPort}/devices`).then((response) => {
      // success callback
      return response.json()
    }, (response) => {
      // TODO error callback
      return [];
    }).then((data) => {
      context.commit('updateNode', {
        id: node.id,
        loading: false,
        devices: data.devices
      });
    });
  }
};

export default {
  state: state,
  mutations: mutations,
  actions: actions
};
