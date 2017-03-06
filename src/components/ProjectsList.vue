<template>
  <md-list class="projects">
    <md-list-item
      v-for="(item, index) in projects" :key="item.project"
      x:href="'https://rawgit.com/marcel-dancak/drums-and-bass/master/dist/latest/index.html#'+item.project"
      :href="'#detail/'+item.id"
      @click.native="showDetail(item)"
      xtarget="_blank">
      <span class="num">{{ index+1 }}</span>
      <md-button
        class="icon-button"
        @click.native.stop.prevent="toggleFavourite(item)">
        <md-icon v-if="item.starred">star</md-icon>
        <md-icon v-else>star_border</md-icon>
      </md-button>
<!--       <a
        class="icon-button"
        @click.stop.prevent="toggleFavourite(item)">
        <md-icon v-if="item.starred">star</md-icon>
        <md-icon v-else>star_border</md-icon>
      </a> -->

      <div class="md-list-text-container">
        <span class="title">{{ item.title }}</span>
        <span>{{ item.artist }}</span>
      </div>
      <a v-if="item.youtube_link"
        class="youtube-link"
        v-bind:href="'https://www.youtube.com/watch?v='+item.youtube_link">
        <i class="fa fa-youtube"></i>
        <p>{{ item.author.name }}</p>
      </a>
    </md-list-item>
  </md-list>
</template>

<script>
export default {
  name: 'projects-list',
  props: {
    projects: {
      type: Array,
      required: true
    },
    toggleFavourite: Function
  },
  methods: {
    showDetail(item) {
      console.log(item.id)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.md-list.projects {
  .md-list-item {
    .icon-button {
      min-width: 36px;
      height: 100%;
      margin: 0;
      /* margin: 0 5px;
      padding: 0 6px;
      border-radius: 50%; */
      &:hover {
        background-color: transparent;
        .md-icon {
          color: #ff5722;
        }
      }
    }
  }
}

.md-list-item:after {
  content: "";
  display: block;
  height: 1px;
  margin: 0 16px;
  background-color: #ddd;
}
.num {
  background-color: #333;
  color: #fff;
  width: 36px;
  height: 36px;
  line-height: 36px;
  text-align: center;
  border-radius: 50%;
  /* margin-right: 12px; */
}
.fa {
  font-size: 28px;
}
a.youtube-link {
  text-align: right;
  color: #555!important;
  line-height: 24px;
  padding: 4px 0;
  &:hover {
    color: #E64A19!important;
    text-decoration: none!important;
  }
  p {
    margin: 2px 0;
    font-size: 14px;
    line-height: 14px;
  }
}
.title {
  font-weight: bold;
  color: #333;
}
</style>
