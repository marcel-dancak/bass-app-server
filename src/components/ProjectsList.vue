<template>
  <md-list class="projects">
    <md-list-item
      v-for="(item, index) in projects" :key="item.project">
      <router-link :to="{ name: 'detail', params: { id: item.id }}">
        <div class="left-section">
          <div class="num">{{ index+1 }}</div>
          <md-icon>{{ item.starred? 'star' : 'star_border' }}</md-icon>
        </div>

        <div class="md-list-text-container">
          <span class="title">{{ item.title }}</span>
          <span>{{ item.artist }}</span>
        </div>

        <div class="right-section2">
          <span class="author">{{ item.author.name }}</span>
          <div class="rating" v-if="item.likes">
            <md-icon>favorite</md-icon>
            <span>{{ item.likes | positive}}</span>
          </div>
          <p class="md-subhead">{{ item.created | timediff }}</p>
        </div>

<!--         <div class="right-section">
          <div class="rating">
            <md-icon>favorite</md-icon>
            <span>{{ item.likes | positive}}</span>
          </div>
          <p class="md-subhead">{{ item.created | timediff }}</p>
        </div> -->

<!--         <a v-if="item.youtube_link"
          class="youtube-link"
          v-bind:href="'https://www.youtube.com/watch?v='+item.youtube_link">
          <i class="fa fa-youtube"></i>
          <p>{{ item.author.name }}</p>
        </a> -->
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
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.md-list.projects {
  .md-list-item {
    .md-list-item-container {
      min-height: 56px;
    }
    .md-icon {
      margin: 0 8px;
    }
    .left-section {
      margin-right: 8px;
      .num {
        display: inline-block;
        display: none;
        font-weight: bold;
        background-color: transparent;
        color: #999;
        width: 18px;
        height: 24px;
        line-height: 24px;
        font-size: 18px;
      }
      .md-icon {
        margin-left: 0;
        font-size: 20px;
        display: inline-block;
        xdisplay: none;
      }
    }
    .right-section2 {
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
        color: #888;
        font-size: 13px;
        line-height: 20px;
      }
    }
    .right-section {
      text-align: right;
      .md-subhead {
        margin: 0;
        color: #888;
        font-size: 14px;
        line-height: 20px;
      }
      .rating {
        display: inline-block;
        position: relative;
        .md-icon {
          font-size: 36px;
          width: 36px;
          margin: 0;
        }
        span {
          position: absolute;
          display: inline-block;
          right: 0;
          width: 36px;
          text-align: center;
          bottom: 0;
          font-size: 12px;
          color: #fff;
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

.num {
  background-color: #444;
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
