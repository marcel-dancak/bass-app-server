<template>
  <div class="page-container md-column">
    <md-card class="header md-warn">
      <md-layout>
        <div class="header-section">

          <md-card-header>
            <div class="md-title">{{ project.title }}</div>
            <div class="md-subhead">{{ project.artist || '-'}}</div>
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

          </md-card-actions>
        </div>
        <div class="author-section">
          <div class="text">
            <span class="md-subhead">created by</span><br />
            <router-link
              class="md-title"
              :to="{ name: 'author', params: { id: project.author.id } }">
              {{ project.author.name }}
            </router-link>
          </div>
          <md-avatar v-if="project.author.avatar" class="md-avatar-icon">
            <img :src="$http.options.root+project.author.avatar">
          </md-avatar>
          <md-avatar v-else class="md-avatar-icon">
            <md-icon>face</md-icon>
          </md-avatar>

          <md-card-actions noauth-disable>
            <!-- <span class="counter">2</span> -->
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
          }
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
      console.log('Detail Created: '+this.id)
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
        console.log('toggle Favourite')
        this.$client.toggleFavourite(project)
      },
      toggleLike(project) {
        console.log('toggle Like')
        this.$client.toggleLike(project)
      },
      toggleSubscribe(author) {
        console.log('toggle Subscribe')
        this.$client.toggleSubscribe(author)
      }
    }
  }
</script>
<style lang="scss">
/*
  .counter {
    padding-left: 6px;
    padding-right: 4px;
  }
*/
  .page-container.md-column {
    display: flex;
    flex-direction: column;
  }
  .nested-page-wrapper {
    position: relative;
    flex: 1 1 auto;
    overflow: visible;
    /* Disable nested scrolling */
    /*
    .page-container {
      overflow: visible!important;
    }
    */
  }

  .md-card.header {
    border-radius: 0;
    .header-section {
      flex: 1 0 auto;
      .md-subhead {
        margin-top: 1px;
      }
      .md-card-actions {
        justify-content: flex-start;
        .md-button {
          padding-left: 6px;
          padding-right: 6px;
          margin-right: 12px;
        }
      }
    }
    .author-section {
      padding: 16px 0 0 16px;
      flex: 0 0 auto;
      .text {
        text-align: right;
        padding-top: 12px;
        display: inline-block;
      }
      .md-avatar {
        float: right;
        width: 56px;
        height: 56px;
        margin: 8px 16px 12px 10px;
        .md-icon {
          width: 64px;
          height: 64px;
          font-size: 64px;
        }
      }
      .md-card-actions {
        width: 100%;
      }
    }
  }
</style>