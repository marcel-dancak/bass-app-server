<template>
  <div>
    <md-toolbar class="md-warn main">
      <slot>Projects</slot>
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
      :showLastEdit="showLastEdit"
      ></projects-table>
    <projects-list v-else :projects="projects"></projects-list>

  </div>
</template>

<script>
import ProjectsList from './ProjectsList'
import ProjectsTable from './ProjectsTable'

export default {
  name: 'responsive-list',
  components: {
    ProjectsList,
    ProjectsTable
  },
  props: {
    projects: {
      type: Array,
      required: true
    },
    showAuthor: Boolean,
    showLastEdit: Boolean
  },
  data () {
    return {
      query: '',
      onDesktop: window.innerWidth >= 720
    }
  },
  created () {
    window.addEventListener('resize', this.handleResize)
    this.query = this.$route.query.q || ''
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    search() {
      const query = Object.assign({}, this.$route.query)
      if (this.query) {
        query['q'] = this.query
      } else {
        delete query.q
      }
      
      this.$router.push({query: query})
    },
    handleResize() {
      this.onDesktop = window.innerWidth >= 720
    }
  }
}
</script>