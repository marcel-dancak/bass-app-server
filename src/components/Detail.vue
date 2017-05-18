<template>
  <div class="page-container detail">
    <md-card class="header md-warn extra-padding-medium">
      <md-layout>
        <div class="header-section">
          <md-card-header>
            <md-layout md-row>
              <md-card-header-text>
                <div class="md-title">{{ project.title }}</div>
                <div class="md-subhead">{{ project.artist || '-'}}</div>
                <div class="md-show-xsmall author-alt">by
                  <router-link class="md-title" :to="{ name: 'author', params: { id: project.author.id } }">
                    {{ project.author.name }}
                  </router-link>
                </div>
              </md-card-header-text>
              <div class="md-hide-xsmall author">
                <span class="md-subhead">created by</span><br />
                <router-link
                  class="md-title"
                  :to="{ name: 'author', params: { id: project.author.id } }">
                  {{ project.author.name }}
                </router-link>
              </div>
              <!-- <span>{{ project.author.name }}</span> -->
              <md-avatar v-if="project.author.avatar" class="md-avatar-icon">
                <img :src="$http.options.media+project.author.avatar">
              </md-avatar>
              <md-avatar v-else class="md-avatar-icon">
                <md-icon class="md-size-3x">face</md-icon>
              </md-avatar>
            </md-layout>
          </md-card-header>

          <md-card-actions noauth-disable>
            <md-button
              class="icon-text"
              :class="{'md-primary': bookmarked}"
              @click.native="toggleBookmark(project)">
              <md-icon>star</md-icon>
              Bookmark
              <!-- &nbsp;<span style="color:#fff">Bookmark</span> -->
            </md-button>

            <md-button
              class="icon-text"
              :class="{'md-primary': liked}"
              @click.native="toggleLike(project)">
              {{ project.likes }}
              <md-icon>thumb_up</md-icon>
              Like
              <!-- &nbsp;<span style="color:#fff">Like</span> -->
            </md-button>

            <span style="flex:1"></span>
            <md-button
              class="icon-text"
              :class="{'md-primary': subscribed}"
              @click.native="toggleSubscribe(project.author)">
                <i class="fa fa-eye"></i> Subscribe
            </md-button>
          </md-card-actions>
        </div>
      </md-layout>
    </md-card>

    <md-divider></md-divider>
    <!-- Content View/Edit sub-page -->
    <div class="nested-page-wrapper">
      <transition name="fade">
        <router-view></router-view>
      </transition>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'detail',
    props: {
      id: String,
    },
    components: {},
    data () {
      return {
        project: {
          id: '',
          title: 'Title',
          artist: 'Artist',
          author: {
            name: 'Author'
          },
          genres: [],
          playing_styles: [],
          tags: []
        }
      }
    },
    computed: {
      liked() {
        return this.$store.state.user.likes.indexOf(this.id) !== -1
      },
      bookmarked() {
        return this.$store.state.user.bookmarks.indexOf(this.id) !== -1
      },
      subscribed() {
        return this.$store.state.user.subscribed.indexOf(this.project.author.id) !== -1
      }
    },
    created() {
      this.fetchData()
    },
    methods: {
      fetchData() {
        this.$client.fetchProject(this.id)
          .then(response => {
            this.project = response.data
          })
      },
      toggleBookmark(project) {
        this.$client.toggleBookmark(project)
      },
      toggleLike(project) {
        this.$client.toggleLike(project)
      },
      toggleSubscribe(author) {
        this.$client.toggleSubscribe(author)
      }
    }
  }
</script>
<style lang="scss">
  .page-container.md-column {
    display: flex;
    flex-direction: column;
  }
  .nested-page-wrapper {
    position: relative;
    flex: 1 1 auto;
    overflow: visible;
    /* Disable nested scrolling */
    .page-container {
      overflow: visible!important;
    }
  }

  .md-card.header {
    border-radius: 0;
    box-shadow: none;

    .header-section {
      flex: 1 0 auto;
      .md-subhead {
        margin-top: 1px;
      }
      .md-card-header {
        padding-top: 21px;
        padding-bottom: 10px;
      }
      .md-card-header-text {
        margin-top: 2px;
      }
      .author {
        text-align: right;
        padding-right: 12px;
        margin-top: 6px;
      }
      .md-card-actions {
        height: 52px;
        .md-button {
          padding-left: 6px;
          padding-right: 6px;
          margin-right: 12px;
          &:last-child {
            margin-right: 6px;
          }
        }
      }
    }
    .author-alt {
      margin-top: 8px;
      a {
        font-size: 16px;
        font-weight: 500;
      }
    }
    .md-avatar-icon {
      width: 62px;
      height: 62px;
      margin-right: 0;
    }
  }
</style>