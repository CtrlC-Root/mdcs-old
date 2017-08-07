import Vue from 'vue';
import Vuex from 'vuex';
import VueRouter from 'vue-router';
import VueResource from 'vue-resource';

import store from './store/index';
import Dashboard from './components/Dashboard.vue';
import Network from './components/Network.vue';
import NodeDetail from './components/node/NodeDetail.vue';
import DeviceDetail from './components/device/DeviceDetail.vue';

// configure Vue plugins
Vue.use(Vuex);
Vue.use(VueRouter);
Vue.use(VueResource);

// create the Vue router
const router = new VueRouter({
  routes: [
    {name: 'dashboard', path: '/', component: Dashboard},
    {name: 'network', path: '/network', component: Network},
    {name: 'node-detail', path: '/node/:node', component: NodeDetail},
    {name: 'device-detail', path: '/node/:node/device/:device', component: DeviceDetail}
  ]
});

// create the Vue application
const app = new Vue({
  store,
  router: router
}).$mount("#app");
