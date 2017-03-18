<template>
  <div class="page-container">
    
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

    <md-card class="detail md-transparent">
      <md-card-content>
        <md-layout md-row md-column-xsmall>
          <md-layout md-flex="70" md-column>
            <md-layout md-row class="actions-toolbar">
              <md-button class="back md-icon-button xmd-fab md-clean" @click.native="back">
                <md-icon>arrow_back</md-icon>
              </md-button>
              <p class="md-subhead">Created: {{ project.created | todate }}</p>
              <div style="flex: 1"></div>
              <!-- <md-layout md-flex="true"></md-layout> -->
              <md-button
                v-if="project.video_link"
                class="fa icon-button md-warn">
                <i class="fa fa-youtube-square"></i>
              </md-button>
              <md-button class="md-primary md-raised open">OPEN</md-button>
            </md-layout>

            <p class="r-pad">
              Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
            </p>
            <!-- <p> {{ project }} </p> -->

          </md-layout>

          <md-layout md-flex="30">
            <md-card class="subcard">
              <p><label>Category: </label> Cover</p>
              <p><label>Genres: </label> {{ project.genres | capitalize-list }}</p>
              <p><label>Techniques: </label> {{ project.playing_styles | capitalize-list }}</p>
              <p>
                <label>Tracks: </label>&nbsp;&nbsp;
                <img
                  v-for="track in project.tracks"
                  class="md-icon md-size-1x"
                  :src="loadImg(track)">
              </p>
            </md-card>
          </md-layout>

        </md-layout>
      </md-card-content>
    </md-card>

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
          title: 'Title',
          artist: 'Artist',
          id: '',
          author: {
            name: 'Author'
          },
          genres: [],
          playing_styles: []
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
      loadImg(name) {
         return require(`../assets/${name}.svg`)
      },
      back() {
        this.$router.go(-1)
      },
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
  .md-card.detail {
    box-shadow: none;
    .md-card-content {
      img.md-icon {
        margin-right: 5px;
      }
      .subcard {
        padding: 6px 16px;
        width: 100%;
      }
    }
    label {
      font-weight: bold;
      color: #444;
      margin-right: 5px;
    }
    .actions-toolbar {
      max-height: 42px;
      .back.md-button {
        min-width: 32px;
        width: 32px;
        .md-icon {
          margin-left: 0;
        }
      }
      i.fa {
        font-size: 36px;
      }
      .md-button {
        margin: 3px 20px;
        height: 36px;
        margin-left: 0;
        &.fa {
          width: 44px;
          min-width: 44px;
          padding: 0;
          opacity: 0.95;
        }
        &.open {
          padding: 0 70px;
        }
      }
      p {
        margin: auto 0;
      }
    }
  }
</style>