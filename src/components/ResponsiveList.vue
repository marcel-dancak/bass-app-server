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

    <md-layout class="paginator" v-if="paginator.has_other_pages">
      <span style="flex:1"></span>
      <md-button
        class="icon-text left"
        :disabled="paginator.page === 1"
        @click.native="setPage(paginator.page-1)">
        <md-icon>keyboard_arrow_left</md-icon>Prev
      </md-button>

      <md-button
        v-for="i in paginator.pages"
        class="page md-raised"
        :class="{ 'md-primary': paginator.page === i }"
        @click.native="setPage(i)">{{ i }}
      </md-button>

      <md-button
        class="icon-text right"
        :disabled="paginator.page === paginator.pages"
        @click.native="setPage(paginator.page+1)">Next
        <md-icon>keyboard_arrow_right</md-icon>
      </md-button>
      <span style="flex:1"></span>
    </md-layout>

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
    paginator: {
      type: Object
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
    setPage(page) {
      // this.paginator.page = page
      // return

      const query = Object.assign({}, this.$route.query)
      query.page = page
      if (page === 1) {
        delete query.page
      }
      this.$router.push({
        path: this.$route.path,
        query: query
      })
    },
    handleResize() {
      this.onDesktop = window.innerWidth >= 720
    }
  }
}
</script>

<style lang="scss">
.paginator {
  .md-button {
    &.page {
      min-width: 34px;
      min-height: 33px;
      height: 33px;
      margin: 6px 4px;
      padding: 0;
    }

    &.icon-text {
      &.left {
        padding-left: 4px;
      }
      &.right {
        padding-right: 4px;
      }
      .md-icon {
        padding-bottom: 2px;
      }
    }
  }
}
</style>