import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

import Dashboard from './Dashboard.vue'
import Network from './Network.vue'

// configure Vue plugins
Vue.use(Vuex)
Vue.use(VueRouter)
Vue.use(VueResource)

// configure Vue default settings
Vue.http.options.root = 'http://127.0.0.1:8000'

// create the data store
const store = new Vuex.Store({
  strict: true,
  state: {
    nextNodeId: 0,
    nodes: []
  },
  mutations: {
    addNode: function (state, node) {
      state.nodes.push(Object.assign({
        id: state.nextNodeId,
        loading: false,
        host: '',
        httpPort: NaN,
        tcpPort: NaN,
        devices: []
      }, node));

      state.nextNodeId++;
    },
    updateNode: function (state, node) {
      // TODO: is there a more efficient way given Vue's reactivity constraints?
      // https://vuejs.org/v2/guide/reactivity.html
      var index = state.nodes.findIndex(function (item) {
        return item.id == node.id;
      });

      var existing = state.nodes[index];
      state.nodes.splice(index, 1);
      state.nodes.push(Object.assign({}, existing, node));
    },
    removeNode: function (state, node) {
      state.nodes = state.nodes.filter(function (item) {
        return item.id != node.id;
      });
    }
  },
  actions: {
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
  }
});

// create the Vue router
const router = new VueRouter({
  routes: [
    {name: 'dashboard', path: '/', component: Dashboard},
    {name: 'network', path: '/network', component: Network}
  ]
})

// create the Vue application
const app = new Vue({
  store,
  router: router,
  http: {
    root: 'http://127.0.0.1:8000/'
  }
}).$mount("#app")
