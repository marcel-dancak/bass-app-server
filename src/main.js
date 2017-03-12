// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.css'
import 'font-awesome/css/font-awesome.css'

import routes from './routes'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

Vue.use(VueRouter)
Vue.use(VueResource)
Vue.use(VueMaterial)


Vue.http.options.root = 'http://localhost:8000'
// Vue.http.options.root = 'http://192.168.0.151:8000'
Vue.http.interceptors.push((request, next) => {
    request.credentials = true;
    next();
})
Vue.material.inkRipple = false


window.app = new Vue({
  el: '#app',
  template: '<router-view></router-view>',
  data: {
    user: {likes: [], favourites: []},
    projects: []
  },
  methods: {
    updateUser(data) {
      Object.assign(this.user, data)
      Object.keys(this.user).forEach(function(key) {
        if (!data[key]) {
          delete this.user[key]
        }
      }, this)
    }
  },
  router: new VueRouter({routes})
})
