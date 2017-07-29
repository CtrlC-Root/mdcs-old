import Vue from 'vue'
import Vuex from 'vuex'

import NodeModule from './node'

// enable the Vuex module
Vue.use(Vuex)

// create and export the store
export default new Vuex.Store({
  strict: true,
  state: {},
  mutations: {},
  actions: {},
  modules: {
    node: NodeModule
  }
});
