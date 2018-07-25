import Vue from 'vue';
import Vuex from 'vuex';
import VueRouter from 'vue-router';
import VueResource from 'vue-resource';

import store from './store/index';
import Network from './components/Dashboard.vue';

// configure Vue plugins
Vue.use(Vuex);
Vue.use(VueRouter);
Vue.use(VueResource);

// create the Vue router
const router = new VueRouter({
  routes: [
    {name: 'dashboard', path: '/', component: Dashboard}
  ]
});

// create the Vue application
const app = new Vue({
  store,
  router: router
}).$mount("#app");
