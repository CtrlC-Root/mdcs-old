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
  state: {
    nextNodeId: 0,
    nodes: []
  },
  mutations: {
    addNode: function (state, node) {
      state.nodes.push({
        id: state.nextNodeId,
        host: node.host,
        httpPort: node.httpPort,
        tcpPort: node.tcpPort
      });

      state.nextNodeId++;
    },
    removeNode: function (state, node) {
      state.nodes = state.nodes.filter(function (item) {
        return item.id != node.id;
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
