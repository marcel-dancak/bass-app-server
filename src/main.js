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

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (const i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

Vue.http.interceptors.push((request, next) => {
    if (request.method === 'POST') {
      const csrftoken = getCookie('csrftoken')
      request.headers.set('X-CSRFTOKEN', csrftoken)
    }
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

Vue.filter('positive', value => {
  return value > 0? value : ''
})

Vue.filter('timediff', value => {
  const time = new Date(value)
  return differenceInDays(new Date(), time)+' days ago'
})

Vue.filter('todate', value => {
  return format(new Date(value), 'MMM D, YYYY')
})

Vue.filter('capitalize', value => {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

Vue.filter('capitalize-list', list => {
  return list.map(item => { return item[0].toUpperCase() + item.slice(1) }).join(', ')
})

Vue.filter('applink', value => {
  const serverUrl = Vue.http.options.root
  return `${serverUrl}/app/#${value}/`
})

Vue.filter('videolink', value => {
  if (value.startsWith('http')) {
    return value
  }
  return 'https://www.youtube.com/watch?v='+value
})

Vue.directive('chips-label', {
  inserted: function (el, binding) {
    let labelEl = document.createElement('label')
    labelEl.appendChild(document.createTextNode(binding.value))
    el.querySelector('.md-input-container').appendChild(labelEl)
  }
})


window.app = new Vue({
  el: '#app',
  template: '<router-view></router-view>',
  router: new VueRouter({routes}),
  store
})
