<template>
  <md-table>

    <md-table-header>
      <md-table-row>
        <md-table-head>Title</md-table-head>
        <md-table-head>Artist</md-table-head>
        <md-table-head>Youtube</md-table-head>
      </md-table-row>
    </md-table-header>

    <md-table-body>
      <md-table-row v-for="(item, index) in projects" :key="item.project">
        <md-table-cell class="title">{{ item.title }}</md-table-cell>
        <md-table-cell>{{ item.author }}</md-table-cell>
        <md-table-cell>
          <a v-if="item.youtube_link"
            v-bind:href="'https://www.youtube.com/watch?v='+item.youtube_link">
            <i class="fa fa-youtube"></i>
          </a>
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
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.md-table-cell {
  text-align: left;
}
.title {
  font-weight: bold;
}
.fa {
  font-size: 28px;
}
a.youtube-link {
  text-align: right;
  color: #555!important;
  line-height: 24px;
  padding: 4px 0;
}
.youtube-link:hover {
  color: #E64A19!important;
  text-decoration: none!important;
}
</style>
