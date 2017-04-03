<template>
  <div class="page-container">
    <responsive-list
      :projects="projects"
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
      showMe: true,
      title: 'Catalog',
      query: '',
      projects: []
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
      if (to.path === '/bookmarked') {
        this.title = 'Bookmarked'
      } else if (to.path === '/liked') {
        this.title = 'Most Liked'
      } else if (to.path === '/created') {
        this.title = 'My Projects'
      } else if (to.path === '/subscribed') {
        this.title = 'From Subscribers'
      } else {
        this.title = 'All Projects'
      }
      this.fetchProjects(to.path, to.query)
      this.query = to.query.q || ''
    },
    fetchProjects(path, query) {
      this.$client.fetchProjects(path, query)
        .then(response => {
          this.projects = response.data
        })
    },
    toggleMenu() {
      this.$emit('toggle-menu')
    }
  }
}
</script>