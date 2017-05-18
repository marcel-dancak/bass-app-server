import Vue from 'vue'
import store from './store'


const CACHE_EXPIRATION = 5 * 60 * 1000

const PROJECTS_FILTERS = {
  projects: '/',
  bookmarked: '/bookmarked/',
  created: '/created/',
  subscribed: '/subscribed/',
  liked: '/liked/'
}

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
    path = 'projects'+(PROJECTS_FILTERS[path] || path)
    const params = {}
    for (const key in query) {
      if (query[key] !== '' && query[key] !== null) {
        params[key] = query[key]
      }
    }
    const data = this.fromCache(path, params)
    if (data) {
      return Vue.Promise.resolve({data: data})
    }
    const q = Vue.http.get(
      path,
      {params: params}
    )
    q.then(response => {
      this.insertToCache(path, params, response.data)
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

  toggleBookmark (project) {
    const user = store.state.user
    const index = user.bookmarks.indexOf(project.id)
    const bookmarked = index === -1
    Vue.http
      .post('bookmark/', {project: project.id, value: bookmarked})
      .then(response => {
          if (bookmarked) {
            user.bookmarks.push(project.id)
          } else {
            user.bookmarks.splice(index, 1)
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
    const index = user.subscribed.indexOf(author.id)
    const subscribed = index === -1
    const q = Vue.http.post('subscribe/', {author: author.id, value: subscribed})
    q.then(response => {
        if (subscribed) {
          user.subscribed.push(author.id)
        } else {
          user.subscribed.splice(index, 1)
        }
        if (author.subscribers_count !== undefined) {
          author.subscribers_count += subscribed? 1 : -1
        }
        // invalidate cache
        this.cache = {}
      }, response => {

      })
    return q
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