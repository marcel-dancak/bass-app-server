<template>
  <div class="page-container">
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
                class="fa icon-button md-warn"
                :href="project.video_link | videolink"
                target="_blank">
                <i class="fa fa-youtube-square"></i>
              </md-button>
              <md-button
                class="md-primary md-raised open"
                :href="project.id | applink"
                target="_blank">
                OPEN
              </md-button>
              <router-link
                v-if="user.username === project.author.name"
                :to="{ path: 'edit' }" append
                class="md-button md-raised md-warn edit md-theme-default">
                <md-icon>edit</md-icon>&nbsp;&nbsp; edit
              </router-link>

<!--               <md-button
                v-if="project.author.name"
                class="md-raised md-warn edit"
                href="#">
                edit <md-icon>edit</md-icon>
              </md-button> -->

<!--               <md-button
                v-if="project.author.name"
                class="fa icon-button md-warn">
                <i class="fa fa-pencil-square"></i>
              </md-button> -->
            </md-layout>

            <p class="r-pad">
              Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
            </p>
            <!-- <p> {{ project }} </p> -->

          </md-layout>

          <md-layout md-flex="30">
            <md-card class="subcard">
              <p><label>Category: </label> {{ project.category }}</p>
              <p><label>Genres: </label> {{ project.genres.join(', ') }}</p>
              <p><label>Techniques: </label> {{ project.playing_styles.join(', ') }}</p>
              <p>
                <label>Tracks: </label>&nbsp;&nbsp;
                <img
                  v-for="track in project.tracks"
                  class="md-icon md-size-1x"
                  :src="loadImg(track)">
              </p>
              <p><label>Difficulty: </label> {{ Difficulties[project.level] }}</p>
            </md-card>
          </md-layout>

        </md-layout>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
  import Constants from '../constants.js'

  export default {
    name: 'detail-content',
    computed: {
      project() {
        return this.$parent.project
      },
      author() {
        return this.$parent.author
      },
      user() {
        return this.$store.state.user
      }
    },
    created() {
      this.Difficulties = Constants.Difficulties
    },
    methods: {
      loadImg(name) {
         return require(`../assets/${name}.svg`)
      },
      back() {
        this.$router.go(-1)
      }
    }
  }
</script>
<style lang="scss">
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
        line-height: 36px;
      }
      i.material-icons {
        margin-bottom: 2px;
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
          padding: 0 60px;
        }
      }
      p {
        margin: auto 0;
      }
    }
  }
</style>