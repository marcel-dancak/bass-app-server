<template>
  <div class="page-container">
    <responsive-list
      :projects="projects"
      :paginator="paginator"
      :showAuthor="showAuthor"
      :showLastEdit="!showAuthor">
      <md-button
        class="menu md-icon-button"
        @click.native="toggleMenu">
        <md-icon>menu</md-icon>
      </md-button>
      <h1 class="md-title">{{ title }}</h1>
    </responsive-list>
  </div>
</template>

<script>
import ResponsiveList from './ResponsiveList'

export default {
  name: 'list',
  components: {
    ResponsiveList
  },
  props: {
    showAuthor: Boolean,
  },
  data () {
    return {
      title: 'Projects',
      projects: [],
      paginator: {page: 1}
    }
  },
  watch: {
    '$route' (to, from) {
      // filter changes when not active (keep-alive)
      if (to.name !== 'list') return

      console.log('** Route changed **')
      this.route(to)
    }
  },
  created () {
    this.route(this.$route)
  },
  methods: {
    route(to) {
      const path = to.path.split('/').pop()
      if (path === 'bookmarked') {
        this.title = 'Bookmarked'
      } else if (path === 'created') {
        this.title = 'My Projects'
      } else if (path === 'subscribed') {
        this.title = 'Subscribed'
      } else {
        this.title = 'All Projects'
      }
      this.fetchProjects(path, to.query)
    },
    fetchProjects(path, query) {
      this.$client.fetchProjects(path, query)
        .then(response => {
          this.projects = response.data.projects || response.data
          this.paginator = response.data.paginator || {page: 1, pages: 3}
        })
    },
    toggleMenu() {
      this.$emit('toggle-menu')
    }
  },
  beforeRouteUpdate (to, from, next) {
    // console.log('beforeRouteUpdate')
    // auto-remove page parameter when changing query
    if (to.query.page && (from.path !== to.path || from.query.page === to.query.page)) {

      delete to.query.page
      next({ path: to.path, query: to.query })
    } else {
      next()
    }
  }
}
</script>