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

    <!-- <projects-list :projects="projects"></projects-list> -->
    <projects-table :projects="projects"></projects-table>

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
    q: String,
    filter: String
  },
  beforeCreate() {
  },
  data () {
    return {
      title: 'Catalog',
      query: '',
      projects: [],
      transition: 'slide-fade-reverse'
    }
  },
  watch: {
    '$route' (to, from) {
      console.log('** Route changed **')
      this.route(to)
    }
  },
  created () {
    this.query = this.q
    this.route(this.$router.currentRoute)
  },
  methods: {
    route(to) {
      if (to.path === '/favourite') {
        this.title = 'Favourite'
      } else if (to.path === '/liked') {
        this.title = 'Most Liked'
      } else if (to.path.startsWith('/author/')) {
        this.title = `Author's Projects`
      } else {
        this.title = 'All Projects'
      }
      this.fetchProjects(to.path, to.query)
    },
    fetchProjects(path, query) {
      // console.log(path+' '+JSON.stringify(query))
      this.$http.get(
        'projects'+path,
        {params: query}
      ).then(response => {
          // get body data
          let projects = response.data;
          let user = this.$root.$data.user

          projects.forEach(function(item) {
            item.starred = user.favourites.indexOf(item.id) !== -1
            item.liked = user.likes.indexOf(item.id) !== -1
          }, this)

          this.projects = projects
          this.$root.$data.projects = projects
        }, response => {
          // error callback
        })
    },
    search() {
      this.$router.push({query: {q: this.query}})
    },
    toggleMenu() {
      this.$emit('toggle-menu')
    }
  }
}
</script>