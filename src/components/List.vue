<template>
  <div class="page-container">
    <md-toolbar class="md-warn main">
      <md-button
        class="menu md-icon-button"
        @click.native="toggleMenu">
        <md-icon>menu</md-icon>
      </md-button>
      <h1 class="md-title">{{ title }}</h1>

      <md-input-container style="flex: 1">
        <md-input
          type="text"
          placeholder="Search"
          v-model="query"
          @keyup.enter.native="search">
        </md-input>
      </md-input-container>

      <md-button
        class="md-icon-button"
        @click.native="search">
        <md-icon>search</md-icon>
      </md-button>
    </md-toolbar>

    <projects-table
      v-if="onDesktop"
      :projects="projects"
      :showAuthor="showAuthor"
      :showLastEdit="!showAuthor"
      ></projects-table>
    <projects-list v-else :projects="projects"></projects-list>

  </div>
</template>

<script>
import ProjectsList from './ProjectsList'
import ProjectsTable from './ProjectsTable'

export default {
  name: 'list',
  components: {
    ProjectsList,
    ProjectsTable
  },
  props: {
    showAuthor: Boolean,
  },
  data () {
    return {
      showMe: true,
      title: 'Catalog',
      query: '',
      projects: [],
      onDesktop: window.innerWidth >= 720
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
    window.addEventListener('resize', this.handleResize)
    this.route(this.$route)
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.handleResize)
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
    search() {
      const query = Object.assign({}, this.$route.query)
      query['q'] = this.query
      this.$router.push({query: query})
    },
    handleResize() {
      this.onDesktop = window.innerWidth >= 720
    },
    toggleMenu() {
      this.$emit('toggle-menu')
    }
  }
}
</script>