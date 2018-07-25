import Vue from 'vue';
import Vuex from 'vuex';

import createPersistedState from 'vuex-persistedstate';

import ActionModule from './action';

// enable the Vuex module
Vue.use(Vuex);

// create and export the store
export default new Vuex.Store({
  strict: true,
  state: {},
  mutations: {},
  actions: {},
  modules: {
    action: ActionModule
  },
  plugins: [createPersistedState()]
});
