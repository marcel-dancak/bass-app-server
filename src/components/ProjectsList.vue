<template>
  <md-list class="projects">
    <md-list-item
      v-for="(item, index) in projects" :key="item.project">
      <router-link :to="{ name: 'detail', params: { id: item.id }}">
        <div class="left-section">
          <md-icon>{{ bookmarks[index]? 'star' : 'star_border' }}</md-icon>
        </div>

        <div class="md-list-text-container">
          <span class="md-title">{{ item.title }}</span>
          <span>{{ item.artist }}</span>
        </div>

        <div class="right-section">
          <span class="author">{{ item.author.name }}</span>
          <div class="rating" v-if="item.likes">
            <md-icon>thumb_up</md-icon>
            <span>{{ item.likes | positive}}</span>
          </div>
          <p class="md-subhead">{{ item.created | timediff }}</p>
        </div>
      </router-link>

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
    }
  },
  computed: {
    bookmarks() {
      return this.projects.map(item => { return this.$store.state.user.favourites.indexOf(item.id) !== -1 })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.md-list.projects {
  .md-list-item {
    .md-button:hover:not([disabled]):not(.md-raised) {
      background-color: #FFF9C4;
    }
    .md-list-item-container {
      min-height: 56px;
    }
    .md-icon {
      margin: 0 8px;
    }
    .left-section {
      margin-right: 8px;
      .md-icon {
        margin-left: 0;
        font-size: 20px;
        display: inline-block;
        xdisplay: none;
      }
    }
    .right-section {
      text-align: right;
      line-height: 26px;
      .rating {
        display: inline-block;
        line-height: 18px;
        .md-icon {
          font-size: 19px;
          min-width: 17px;
          width: 17px;
          min-height: 19px;
          height: 19px;
          margin: 0;
        }
        &:before {
          content: "/";
          color: #aaa;
          padding: 0 2px;
        }
        span {
          font-size: 13px;
        }
      }
      .author {
        margin: 0;
        font-size: 15px;
        line-height: 20px;
        font-weight: 500;
        color: #444;
      }
      .md-subhead {
        margin: 0;
        opacity: 0.6;
        font-size: 13px;
        line-height: 20px;
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
.md-list-item:hover {
  &:before {
    position: absolute;
    top: -1px;
    left: 0;
    right: 0;
    content: "";
    display: block;
    height: 1px;
    background-color: #ddd;
  }
  &:after {
    margin: 0;
  }
}

</style>
