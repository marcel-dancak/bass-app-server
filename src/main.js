// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.css'
import 'font-awesome/css/font-awesome.css'

import store from './store'
import routes from './routes'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import Client from './client'

Vue.use(VueRouter)
Vue.use(VueResource)
Vue.use(VueMaterial)
Vue.use(Client)

Vue.http.options.root = process.env.API_URL

Vue.http.interceptors.push((request, next) => {
    request.credentials = true;
    next();
})
Vue.material.inkRipple = false

// TODO: use 'dark' theme on headers when bug in Vue-Material (hue in accent)
// will be fixed
Vue.material.registerTheme({
  'default': {
    primary: 'blue',
    accent: 'blue-grey',
    warn: {
      color: 'blue-grey',
      hue: 800
    }
  },
  dark: {
    primary: 'blue',
    accent: {
      color: 'blue-grey',
      hue: 800
    }
  }
})

import differenceInMinutes from 'date-fns/difference_in_minutes'
import differenceInDays from 'date-fns/difference_in_days'
import differenceInWeeks from 'date-fns/difference_in_weeks'
import format from 'date-fns/format'

Vue.filter('positive', function(value) {
  return value > 0? value : ''
})

Vue.filter('timediff', function(value) {
  const time = new Date(value)
  return differenceInDays(new Date(), time)+' days ago'
})

Vue.filter('todate', function(value) {
  const time = new Date(value)
  return format(time, 'MMM D, YYYY')
})

Vue.filter('capitalize-list', function(list) {
  return list.map(item => { return item[0].toUpperCase() + item.substr(1) }).join(', ')
})


window.app = new Vue({
  el: '#app',
  template: '<router-view></router-view>',
  router: new VueRouter({routes}),
  store
})
