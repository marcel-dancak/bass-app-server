<template>
  <md-table>

    <md-table-header>
      <md-table-row>
        <md-table-head class="icon"></md-table-head>
        <md-table-head class="title">Title
          <md-chips
            v-model="filter.artists"
            :md-input-placeholder="filter.artists.length? ' ' : 'Artist filter'"
            @change="updateFilter">
            <template scope="chip">{{ chip.value }}</template>
          </md-chips>
        </md-table-head>
        <md-table-head>Genre
          <md-chips
            v-model="filter.genres"
            :md-input-placeholder="filter.genres.length? ' ' : 'Genre filter'"
            @change="updateFilter">
            <template scope="chip">{{ chip.value }}</template>
          </md-chips>
        </md-table-head>
        <md-table-head>Playing style
          <md-chips
            v-model="filter.styles"
            :md-input-placeholder="filter.styles.length? ' ' : 'Style filter'"
            @change="updateFilter">
            <template scope="chip">{{ chip.value }}</template>
          </md-chips>
        </md-table-head>
        <md-table-head>Author</md-table-head>
        <md-table-head class="icon"><md-icon>thumb_up</md-icon></md-table-head>
      </md-table-row>
    </md-table-header>

    <md-table-body>
      <md-table-row v-for="(item, index) in projects" :key="item.project">
        <md-table-cell class="icon">
          <md-icon>{{ item.starred? 'star' : 'star_border' }}</md-icon>
        </md-table-cell>
        <md-table-cell class="title">
          <router-link :to="{ name: 'detail', params: { id: item.id }}">
            <div class="md-title">{{ item.title }}</div>
            <div class="md-subhead">{{ item.artist }}</div>
          </router-link>
        </md-table-cell>
        <md-table-cell>{{ item.genres.join(', ') }}</md-table-cell>
        <md-table-cell>{{ item.playing_styles.join(', ') }}</md-table-cell>
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
        styles: []
      }
    }
  },
  methods: {
    updateFilter() {
      console.log('updateFilter')
      const current = this.$router.currentRoute
      let query = {}
      for (let key in this.filter) {
        const values = this.filter[key]
        if (values.length) {
          query[key] = values.join(',')
        }
      }
      this.$router.push({
        path: current.path,
        query: query
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
.md-table {
  .md-table-header {
    background-color: #EEEEEE;
    tr {
      border-bottom: 1px solid #ccc;
    }
  }
  .md-table-head.icon {
    min-width: 24px;
    width: 24px;
  }
  .md-table-head {
    height: 80px;
    .md-table-head-container {
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
      /*
      position: relative;
      width: 100%;
      height: 72px;
      .md-chips {
        position: absolute;
        left: 16px;
        right: 0;
        top: 32px;
      }
      */
    }
    &.title .md-table-head-text {
      padding-left: 0;
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
        padding: 0 15px;
      }
    }
    &.title {
      line-height: 22px;
      .md-table-cell-container {
        padding-left: 0;
      }
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
  .md-table-row:hover .md-table-cell {
    background-color: #FFF9C4!important;
  }
}
</style>
