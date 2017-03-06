// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.css'
import 'font-awesome/css/font-awesome.css';

import VueResource from 'vue-resource';

Vue.use(VueResource)
Vue.use(VueMaterial)
// Vue.use(VueMaterial.MdCore)
// Vue.use(VueMaterial.MdButton)


Vue.http.options.root = 'http://localhost:8000'
// Vue.http.options.root = 'http://192.168.0.151:8000'
Vue.http.interceptors.push((request, next) => {
    request.credentials = true;
    next();
})
Vue.material.inkRipple = false
/* eslint-disable no-new */
window.app = new Vue({
  el: '#app',
  template: '<App/>',
  components: { App },
  data: {
    seen: true
  }
})

// import routes from './routes'

// const app = new Vue({
//   el: '#app',
//   data: {
//     currentRoute: window.location.pathname
//   },
//   computed: {
//     ViewComponent () {
//       const matchingView = routes[this.currentRoute]
//       console.log(this.currentRoute+' -> '+matchingView)
//       return matchingView
//         ? require('./' + matchingView + '.vue')
//         : require('./App.vue')
//     }
//   },
//   render (h) {
//     return h(this.ViewComponent)
//   }
// })

// window.addEventListener('popstate', () => {
//   app.currentRoute = window.location.pathname
// })
