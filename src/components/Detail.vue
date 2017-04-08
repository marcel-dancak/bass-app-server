<template>
  <div class="page-container md-column">
    <md-card class="header md-warn">
      <md-layout>
        <div class="header-section">
          <md-card-header>
            <md-layout md-row>
              <div>
                <div class="md-title">{{ project.title }}</div>
                <div class="md-subhead">{{ project.artist || '-'}}</div>
                <div class="md-show-xsmall author-alt">by
                  <router-link class="md-title" :to="{ name: 'author', params: { id: project.author.id } }">
                    {{ project.author.name }}
                  </router-link>
                </div>
              </div>
              <div style="flex:1"></div>
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
                <img :src="$http.options.root+project.author.avatar">
              </md-avatar>
              <md-avatar v-else class="md-avatar-icon">
                <md-icon>face</md-icon>
              </md-avatar>
            </md-layout>
          </md-card-header>

          <md-card-actions noauth-disable>
            <md-button
              class="icon-text"
              :class="{'md-primary': bookmarked}"
              @click.native="toggleFavourite(project)">
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
        return this.$store.state.user.favourites.indexOf(this.id) !== -1
      },
      subscribed() {
        return this.$store.state.user.subscribers.indexOf(this.project.author.id) !== -1
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
      toggleFavourite(project) {
        this.$client.toggleFavourite(project)
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

    .md-card-header {
      padding-top: 24px;
      padding-bottom: 13px;
    }

    .author {
      text-align: right;
      padding-right: 12px;
    }

    .header-section {
      flex: 1 0 auto;
      .md-subhead {
        margin-top: 1px;
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
      width: 56px;
      height: 56px;
      margin-right: 0;
    }
  }
</style>