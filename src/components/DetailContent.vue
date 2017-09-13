<template>
  <div class="page-container extra-padding-medium">
    <md-card class="detail md-transparent" style="overflow:visible">
      <md-card-content>
        <md-layout md-row md-column-xsmall>
          <md-layout
            md-column md-flex="65" md-flex-small="60"
            class="left-block">
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

            <!-- <p style="white-space:pre-line">{{ project.description }}</p> -->
            <p class="description" v-html="compiledMarkdown"></p>

          </md-layout>
          <!-- <span class="md-flex"></span> -->
          <md-layout md-column md-flex>
            <md-card class="subcard">
              <div class="triangle-label"><span>{{ project.category }}</span></div>
              <table>
                <col width="33%">
                <tbody>
                  <tr>
                    <td>Difficulty</td>
                    <td><level-indicator :value="project.level"></level-indicator></td>
                  </tr>
                  <tr>
                    <td>Genres</td>
                    <td>{{ project.genres.join(', ') }}</td>
                  </tr>
                  <tr>
                    <td>Techniques</td>
                    <td>{{ project.playing_styles.join(', ') }}</td>
                  </tr>
                  <tr v-if="project.tags.length">
                    <td>Tags</td>
                    <td>{{ project.tags.join(', ') }}</td>
                  </tr>
                  <tr>
                    <td>Tracks</td>
                    <td>
                      <img
                        v-for="track in project.tracks"
                        class="md-icon md-size-1x"
                        :src="loadImg(track)">
                    </td>
                  </tr>
                </tbody>
              </table>
            </md-card>
          </md-layout>

        </md-layout>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
  import Constants from '../constants.js'
  import LevelIndicator from './LevelIndicator.vue'

  import marked from 'marked'

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
      },
      compiledMarkdown: function () {
        if (this.project.description) {
          return marked(this.project.description, { sanitize: false })
        }
        return 'No description provided.'
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

  .description {
    div, p {
      margin: 12px 0 8px 0;
    }
    h1 {
      font-size: 20px;
    }
    h2, h3 {
      font-size: 17px;
    }
    /*
    h2 ~ p {
      margin-top: 8px;
    }*/

    ul>li+li,
    ol>li+li {
      margin-top: 4px;
    }
    ul>li>p,
    ol>li>p {
      margin: 0;
    }
  }

  .md-card.detail {
    box-shadow: none;
    background: none;
    small {
      xopacity: 0.95;
      font-size: 12px;
      xfont-weight: normal;
    }
    .md-card-content {
      height: auto;
      .left-block {
        /* fixes height on safari */
        @media (max-width: 600px) {
          flex: 1 1 auto;
        }
        @media (min-width: 600px) {
          padding-right: 16px;
        }
        @media (min-width: 1024px) {
          padding-right: 44px;
        }
      }
      .created {
        font-weight: 500;
        opacity: 0.85;
      }
      img.md-icon {
        margin-right: 6px;
      }
      .subcard {
        padding: 6px 16px;
        width: 100%;
        overflow-x: hidden;
        table {
          width: 100%;
          tr {
            line-height: 22px;
            td {
              padding: 11px 0;
            }
            > td:first-child {
              min-width: 92px;
              font-weight: 500;
              color: #444;
            }
          }
        }
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
  }
</style>