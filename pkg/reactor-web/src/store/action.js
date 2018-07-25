import Vue from 'vue';

const state = {
  all: []
};

const getters = {
};

const mutations = {
  addAction: function (state, action) {
    state.all.push(Object.assign({
      uuid: '',
      name: '',
      description: '',
      content: '',
    }, action));
  },

  updateAction: function (state, action) {
    // TODO: is there a more efficient way given Vue's reactivity constraints?
    // https://vuejs.org/v2/guide/reactivity.html
    var index = state.all.findIndex(function (item) {
      return item.uuid == node.uuid;
    });

    var existing = state.all[index];
    state.all.splice(index, 1);
    state.all.push(Object.assign({}, existing, action));
  },

  removeAction: function (state, action) {
    state.all = state.all.filter(function (item) {
      return item.uuid != node.uuid;
    });
  }
};

const actions = {
  fetchActions: function (context, params) {
    return Vue.http.get(`http://${params.reactorUrl}/action/`).then((response) => {
      return response.json();
    }).then((actions) => {
      actions.forEach((action) => {
        context.commit('addAction', action);
      });

      return actions;
    });
  },
};

export default {
  state: state,
  getters: getters,
  mutations: mutations,
  actions: actions
};
