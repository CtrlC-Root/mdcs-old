import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

import store from './store/index'
import Dashboard from './Dashboard.vue'
import Network from './Network.vue'

// configure Vue plugins
Vue.use(Vuex)
Vue.use(VueRouter)
Vue.use(VueResource)

// configure Vue default settings
Vue.http.options.root = 'http://127.0.0.1:8000'

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
  http: {}
}).$mount("#app")
