<template>
  <md-table>
    <md-table-header>
      <md-table-row>
        <md-table-head class="icon noauth-hide"></md-table-head>
        <md-table-head class="title">Title
          <md-chips
            v-model="filter.artists"
            :md-input-placeholder="filter.artists.length? 'Add' : 'Artist filter'"
            @change="updateFilter">
            <template scope="chip">{{ chip.value }}</template>
          </md-chips>
        </md-table-head>
        <md-table-head>Genre
          <md-chips
            class="capitalize"
            v-model="filter.genres"
            :md-input-placeholder="filter.genres.length? 'Add' : 'Genre filter'"
            @change="updateFilter">
            <template scope="chip">{{ chip.value }}</template>
          </md-chips>
        </md-table-head>
        <md-table-head>Playing style
          <md-chips
            class="capitalize"
            v-model="filter.styles"
            :md-input-placeholder="filter.styles.length? 'Add' : 'Style filter'"
            @change="updateFilter">
            <template scope="chip">{{ chip.value }}</template>
          </md-chips>
        </md-table-head>
        <md-table-head>Author
          <md-chips
            v-model="filter.authors"
            :md-input-placeholder="filter.authors.length? 'Add' : 'Author filter'"
            @change="updateFilter">
            <template scope="chip">{{ chip.value }}</template>
          </md-chips>
        </md-table-head>
        <md-table-head class="slim"><md-icon>thumb_up</md-icon></md-table-head>
      </md-table-row>
    </md-table-header>

    <md-table-body>
      <md-table-row v-for="(item, index) in projects" :key="item.project">
        <md-table-cell class="icon noauth-hide">
          <!-- <md-icon>{{ item.starred? 'star' : 'star_border' }}</md-icon> -->
          <md-icon>{{ bookmarks[index]? 'star' : 'star_border' }}</md-icon>
        </md-table-cell>
        <md-table-cell class="title">
          <router-link :to="{ name: 'detail', params: { id: item.id }}">
            <div class="md-title">{{ item.title }}</div>
            <div class="md-subhead">{{ item.artist }}</div>
          </router-link>
        </md-table-cell>
        <md-table-cell>{{ item.genres | capitalize-list }}</md-table-cell>
        <md-table-cell>{{ item.playing_styles | capitalize-list }}</md-table-cell>
        <md-table-cell class="author">
          <div class="md-title">{{ item.author.name }}</div>
          <div class="md-subhead">{{ item.created | timediff }}</div>
        </md-table-cell>
        <md-table-cell>
          {{ item.likes }}
        </md-table-cell>
      </md-table-row>
    </md-table-body>

  </md-table>
</template>

<script>
export default {
  name: 'projects-table',
  props: {
    projects: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      filter: {
        artists: [],
        genres: [],
        styles: [],
        authors: []
      }
    }
  },
  computed: {
    bookmarks() {
      return this.projects.map(item => { return this.$store.state.user.favourites.indexOf(item.id) !== -1 })
    }
  },
  methods: {
    updateFilter() {
      console.log('updateFilter')
      let query = {}
      for (let key in this.filter) {
        const values = this.filter[key]
        if (values.length) {
          query[key] = values.join(',').toLowerCase()
        }
      }
      this.$router.push({
        path: this.$route.path,
        query: query
      })
    },
    syncWithRoute(route) {
      for (let key in this.filter) {
        this.filter[key] = route.query[key]? route.query[key].split(',') : []
      }
    }
  },
  created() {
    this.syncWithRoute(this.$route)
  },
  watch: {
    '$route' (to, from) {
      // TODO: filter when not active
      console.log('## Route changed ##')
      this.syncWithRoute(to)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
.md-table {
  .md-table-row:hover .md-table-cell {
    background-color: #FFF9C4!important;
  }
  .md-table-header {
    tr {
      border-bottom: 1px solid #ccc;
    }
  }

  .md-table-head {
    height: 80px;

    &.icon {
      width: 32px;
      .md-table-head-container {
        width: inherit;
      }
    }
    &.slim {
      width: 64px;
      .md-table-head-container {
        width: inherit;
      }
    }
    .md-table-head-container {
      background-color: #EEEEEE!important;
      height: 80px;
      padding: 8px 0;
    }
    .md-input-container {
      margin: 0;
      padding-top: 4px;
      height: 36px;
      min-height: 36px;
      .md-input {
        font-size: 14px;
        &::-webkit-input-placeholder {
          font-size: 14px;
          opacity: 0.55;
        }
      }
    }
    .md-chip {
      height: 26px;
      line-height: 12px;
      .md-button.md-delete {
        top: 2px;
      }
    }
    .md-table-head-text {
      height: auto;
      font-size: 14px;
      .md-chips.capitalize {
        text-transform: capitalize;
      }
      /* make input field short when not empty */
      .md-chips .md-chip + .md-input {
        width: 64px;
      }
    }
  }

  .md-table-cell {
    padding: 0;
    font-size: 14px;

    .md-table-cell-container {
      padding-top: 4px;
      padding-bottom: 4px;
    }
    &.icon {
      .md-table-cell-container {
        padding: 0 8px;
        opacity: 0.75;
        width: 32px;
        justify-content: flex-end;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        .md-icon {
          font-size: 20px;
          min-width: 0;
          width: 20px;
          margin: 0;
        }
      }
    }
    &.title {
      line-height: 22px;
      a {
        width: 100%;
      }
      .md-title {
        font-size: 18px;
        color: #444;
      }
      .md-subhead {
        font-size: 13px;
        color: #888;
      }
    }
    &.author {
      .md-title {
        font-size: 15px;
        color: #444;
      }
      .md-subhead {
        font-size: 13px;
        color: #888;
      }
    }
  }
}
</style>
