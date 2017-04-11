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
      title: 'Projects',
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
      const path = to.path.split('/').pop()
      console.log(path)
      if (path === 'bookmarked') {
        this.title = 'Bookmarks'
      } else if (path === 'liked') {
        this.title = 'Highest Rated'
      } else if (path === 'created') {
        this.title = 'My Projects'
      } else if (path === 'subscribed') {
        this.title = 'Watched'
      } else {
        this.title = 'All Projects'
      }
      this.fetchProjects(path, to.query)
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