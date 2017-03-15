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
Vue.material.registerTheme({
  'default': {
    primary: 'blue',
    accent: 'blue-grey',
    warn: {
      color: 'blue-grey',
      hue: 800
    }
  },
  author: {
    accent: {
      color: 'blue',
      hue: 200
    },
    // warn: {
    //   color: 'blue',
    //   hue: 300
    // },
    warn: {
      color: 'blue-grey',
      hue: 600
    },
    primary: {
      color: 'blue-grey',
      hue: 800
    }
  },
  detail: {
    primary: 'blue',
    accent: 'white',
    warn: {
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
