<template>
  <div class="page-container">
    <md-card class="detail md-transparent">
      <md-card-content>
        <md-layout md-row md-column-xsmall>
          <md-layout md-flex="65" md-column md-flex-small="60" class="r-pad">
            <md-layout md-row md-column-small class="actions-toolbar">
              <md-layout md-row>
                <md-button
                  class="back md-icon-button md-clean"
                  @click.native="$router.back">
                  <md-icon>arrow_back</md-icon>
                </md-button>&nbsp;&nbsp;
                <span class="created">
                  <!-- <md-icon>file_upload</md-icon>&nbsp; -->
                  Published:&nbsp;
                  {{ project.created | todate }}
                </span>
              </md-layout>
              <md-layout md-row md-align="end">
                <md-button
                  v-if="project.video_link"
                  class="fa icon-button md-warn"
                  :href="project.video_link | videolink"
                  target="_blank">
                  <i class="fa fa-youtube-square"></i>
                </md-button>
                <md-button
                  class="md-primary md-raised open md-flex-small"
                  :href="project.id | applink"
                  target="_blank">
                  OPEN
                </md-button>
                <router-link
                  v-if="user.username === project.author.name"
                  :to="{ path: 'edit' }" append
                  class="md-button md-raised md-warn edit md-theme-default md-flex-small">
                  <md-icon>edit</md-icon>&nbsp;&nbsp; edit
                </router-link>
              </md-layout>
            </md-layout>

            <p>
              {{ project.description }}
            </p>

          </md-layout>

          <md-layout md-flex="35" md-flex-small="40" xmd-column>
            <md-card class="subcard md-align-center">
<!--               <p><label>Difficulty: </label>
                <span class="level"> {{ Difficulties[project.level] }}</span>
              </p> -->
              <!-- <div class="triangle-label" :level="project.level">{{ Difficulties[project.level] }}</div> -->
              <div class="triangle-label"><span>{{ project.category }}</span></div>

              <!-- <p><label>Category: </label> {{ project.category }}</p> -->
<!--               <p><label>Difficulty: </label>
                {{ Difficulties[project.level].numeric }}
                <small>({{ Difficulties[project.level].title }})</small>
              </p> -->
              <p style="margin-bottom:5px">
                <label>Difficulty: </label>
                <level-indicator :value="project.level"></level-indicator>
              </p>
              <!-- <p><label>Difficulty: </label>
                {{ Difficulties[project.level].title }}
                &nbsp;( {{ Difficulties[project.level].numeric }} / 5 )
              </p> -->

              <p><label>Genres: </label> {{ project.genres.join(', ') }}</p>
              <p><label>Techniques: </label> {{ project.playing_styles.join(', ') }}</p>
              <p v-if="project.tags.length">
                <label>Tags: </label> {{ project.tags.join(', ') }}
              </p>
              <p>
                <label>Tracks: </label>
                <img
                  v-for="track in project.tracks"
                  class="md-icon md-size-1x"
                  :src="loadImg(track)">
              </p>
            </md-card>
            <!-- <div style="flex:1"></div> -->
            <!-- <md-layout md-flex></md-layout> -->
          </md-layout>

        </md-layout>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
  import Constants from '../constants.js'
  import LevelIndicator from './LevelIndicator.vue'
  export default {
    name: 'detail-content',
    components: {
      LevelIndicator
    },
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
      }
    }
  }
</script>
<style lang="scss">
  @import '../variables.scss';

  .md-card.detail {
    box-shadow: none;
    small {
      xopacity: 0.95;
      font-size: 12px;
      xfont-weight: normal;
    }
    .md-card-content {
      .created {
        font-weight: bold;
        opacity: 0.85;
      }
      img.md-icon {
        margin-right: 6px;
      }
      .subcard {
        padding: 6px 16px;
        width: 100%;
        min-width: 240px;
        overflow-x: hidden;
        p {
          margin: 12px 0;
        }
        .level {
          background-color: #37474f;
          xbackground-color: #555;
          color: #fff;
          opacity: 0.85;
          text-transform: uppercase;
          font-weight: bold;
          font-size: 12px;
          padding: 3px 6px 2px 6px;
          line-height: 12px;
          border-radius: 4px;
        }
      }
    }
    label {
      font-weight: 500;
      color: #444;
      margin-right: 5px;
      min-width: 92px;
      width: 33%;
      display: inline-block;
    }
    .actions-toolbar {
      min-height: 48px;
      line-height: 38px;
      border-bottom: 1px solid #ddd;
      flex: 0 0 auto;
      justify-content: space-between;
      > .md-row {
        height: 48px;
        flex: 0 0 auto;
      }
      .back.md-button {
        margin-left: 0!important;
        min-width: 32px;
        width: 32px;
        .md-icon {
          margin-left: 0;
          margin-bottom: auto;
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
        margin: 0 3px 6px 6px!important;
        height: 36px;
        margin-left: 0;
        &.fa {
          width: 44px;
          min-width: 44px;
          padding: 0;
          opacity: 0.95;
        }
        @media (min-width: 480px) {
          min-width: 130px;
        }
      }
      p {
        margin: auto 0;
      }
    }
    .triangle-label {
      color: #fff;
      font-weight: 500;
      position: absolute;
      text-align: center;

      top: -13px;
      right: -34px;
      height: 60px;
      width: 100px;
      line-height: 92px;
      transform: rotate(45deg);

      transform: rotate(35deg);
      width: 108px;
      top: -22px;
      right: -27px;
      padding-left: 5px;

      height: 32px;
      top: 3px;
      right: -24px;
      line-height: 42px;
      box-shadow: $material-shadow-2dp;

      top: 5px;
      right: -24px;
      width: 132px;
      height: 38px;
      padding-left: 10px;
      line-height: 18px;
      font-size: 13px;
      display: table;
      xbackground-color: #424242;
      background-color: #EEEEEE;
      color: #616161;
      opacity: 0.75;

      span {
        display: table-cell;
        vertical-align: middle;
        word-spacing: 120px;
      }
    }
    .triangle-label[level="1"] {
      background-color: #689F38;
      xline-height: 95px;
    }
    .triangle-label[level="2"] {
      background-color: #AFB42B;
    }
    .triangle-label[level="3"] {
      background-color: #FFA000;
    }
    .triangle-label[level="4"] {
      background-color: #E64A19;
    }
    .triangle-label[level="5"] {
      background-color: #d32f2f;
    }
    .triangle-label[level="6"] {
      background-color: #5D4037;
    }
  }
</style>