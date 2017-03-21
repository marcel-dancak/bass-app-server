import Vue from 'vue'
import store from './store'


const CACHE_EXPIRATION = 5 * 60 * 1000

class Client {

  cache = {}

  insertToCache (path, query, data) {
    const key = path+JSON.stringify(query)
    this.cache[path] = {
      key: key,
      time: Date.now(),
      data: data
    }
  }

  fromCache (path, query) {
    console.log('Searching in cache: '+path)
    console.log(Object.keys(this.cache))
    const key = path+JSON.stringify(query)
    const record = this.cache[path]
    if (record && record.key === key && Date.now()-record.time < CACHE_EXPIRATION) {
      return record.data
    }
  }

  projectFromCache (id) {
    for (const key in this.cache) {
      console.log('searching in cache: '+key)
      const projects = this.cache[key].data.projects || this.cache[key].data
      const project = projects.find(p => { return p.id === id })
      if (project) {
        return project
      }
    }
  }

  // projectFromCacheAll (id) {
  //   let list = []
  //   for (const key in this.cache) {
  //     console.log('searching in cache: '+key)
  //     const projects = this.cache[key].data.projects || this.cache[key].data
  //     const project = projects.find(p => { return p.id === id })
  //     if (project) {
  //       list.push(project)
  //     }
  //   }
  //   return list
  // }

  fetchProjects (path, query) {
    if (!path.endsWith('/')) {
      path = path+'/'
    }
    const data = this.fromCache(path, query)
    if (data) {
      return Vue.Promise.resolve({data: data})
    }
    const q = Vue.http.get(
      'projects'+path,
      {params: query}
    )
    q.then(response => {
      this.insertToCache(path, query, response.data)
    })
    return q
  }

  fetchUserProjects (id, query) {
    const path = `/author/${id}/`
    return this.fetchProjects(path, query)
  }

  fetchProject (id) {
    const project = this.projectFromCache(id)
    if (project) {
      return Vue.Promise.resolve({data: project})
    }
    return Vue.http.get('project/', { params: {id: id} })
  }

  updatePorject (data) {
    const q = Vue.http.post('project/', data)
    q.then(response => {
      this.cache = {}
    })
    return q
  }

  toggleFavourite (project) {
    const user = store.state.user
    const index = user.favourites.indexOf(project.id)
    const bookmarked = index === -1
    Vue.http
      .post('star/', {project: project.id, value: bookmarked})
      .then(response => {
          if (bookmarked) {
            user.favourites.push(project.id)
          } else {
            user.favourites.splice(index, 1)
          }
        }, response => {

        })
  }

  toggleLike (project) {
    const user = store.state.user
    const index = store.state.user.likes.indexOf(project.id)
    const liked = index === -1
    Vue.http
      .post('like/', {project: project.id, value: liked})
      .then(response => {
          if (liked) {
            user.likes.push(project.id)
            project.likes++
          } else {
            user.likes.splice(index, 1)
            project.likes--
          }
          // update 'likes' property in all cached projects
          // this.projectFromCacheAll(project.id)
          //   .forEach(item => { item.likes = project.likes })

          // or invalidate cache?
          this.cache = {}
        }, response => {

        })
  }

  toggleSubscribe(author) {
    const user = store.state.user
    const index = user.subscribers.indexOf(author.id)
    const subscribed = index === -1
    Vue.http
      .post('subscribe/', {author: author.id, value: subscribed})
      .then(response => {
          if (subscribed) {
            user.subscribers.push(author.id)
          } else {
            user.subscribers.splice(index, 1)
          }
        }, response => {

        })
  }

  loadUserProfile() {
    const q = Vue.http.get('profile/')
    q.then(response => {
        store.commit('updateProfile', response.data)
      }, response => {})
    return q
  }

}

const ClientPlugin = {
  install(Vue, options) {
    Vue.prototype.$client = new Client()
  }
}

export default ClientPlugin