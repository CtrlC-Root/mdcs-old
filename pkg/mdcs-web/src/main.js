import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

import Dashboard from './Dashboard.vue'
/*
import ContentList from './ContentList.vue'
import ContentDetail from './ContentDetail.vue'
import TagList from './TagList.vue'
import TagDetail from './TagDetail.vue'
*/

// configure Vue plugins
Vue.use(VueRouter)
Vue.use(VueResource)

// configure Vue default settings
Vue.http.options.root = 'http://127.0.0.1:8000'

// create the Vue router
const router = new VueRouter({
  routes: [
    {name: 'dashboard', path: '/', component: Dashboard}
  ]
})

// create the Vue application
const app = new Vue({
  router: router,
  http: {
    root: 'http://127.0.0.1:8000/'
  }
}).$mount("#app")