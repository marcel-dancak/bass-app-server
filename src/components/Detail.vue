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
              </md-card-header-text>
              <div class="md-hide-xsmall author">
                <span class="md-subhead">created by</span><br />
                <router-link
                  class="md-title"
                  :to="{ name: 'author', params: { id: project.author.id } }">
                  {{ project.author.name }}
                </router-link>
              </div>
              <router-link :to="{ name: 'author', params: { id: project.author.id } }">
                <md-avatar v-if="project.author.avatar" class="md-avatar-icon">
                  <img :src="$http.options.media+project.author.avatar">
                </md-avatar>
                <md-avatar v-else class="md-avatar-icon">
                  <md-icon class="md-size-3x">face</md-icon>
                </md-avatar>
                <div class="md-show-xsmall text-center">{{ project.author.name }}</div>
              </router-link>

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
        padding-top: 1.313rem;
        padding-bottom: 0.625rem;
      }
      .md-card-header-text {
        margin-top: 2px;
      }
      .author {
        text-align: right;
        padding-right: 0.75rem;
        margin-top: 0.375rem;;
      }
      .md-card-actions {
        height: 3.25rem;
        padding: 0.5rem;
        .md-button {
          padding-left: 0.375rem;
          padding-right: 0.375rem;
          margin-right: 0.75rem;
          &:last-child {
            margin-right: 0.375rem;;
          }
        }
      }
    }
    a {
      text-align: right;
      .md-avatar {
        float: none;
      }
    }
    .md-avatar-icon {
      width: 3.875rem;
      height: 3.875rem;
      margin-right: 0;
    }
  }
</style>