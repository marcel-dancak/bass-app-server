<template>
  <div>
    <md-toolbar class="md-warn main">
      <md-button href="#">
        <md-icon>arrow_back</md-icon> Back
      </md-button>
      <!-- <h3 class="md-title">About</h3> -->
    </md-toolbar>
    
    <md-card class="project">

      <md-layout md-column-xsmall>
        <div class="header-section">
          <md-card-header>
            <div class="md-title">{{ project.title }}</div>
            <div class="md-subhead">{{ project.artist || '-'}}</div>
          </md-card-header>
          <md-card-actions>
            <md-button
              class="icon-text"
              @click.native="toggleFavourite(project)">
              <md-icon v-if="project.starred">star</md-icon>
              <md-icon v-else>star_border</md-icon>
              Bookmark
            </md-button>

            <span class="counter">{{ project.likes }}</span>
<!--             <md-button
              class="icon-text"
              :class="{active: project.liked}"
              @click.native="toggleLike(project)">
              <md-icon>thumb_up</md-icon> Like
            </md-button> -->

            <md-button
              class="icon-text"
              @click.native="toggleLike(project)">
              <template v-if="project.liked">
                <md-icon class="active">thumb_up</md-icon> Unlike
              </template>
              <template v-else>
                <md-icon>thumb_up</md-icon> Like
              </template>
            </md-button>

          </md-card-actions>
        </div>
        <div class="author-section">
          <div class="text">
            <span class="md-subhead">created by</span><br />
            <a :href="'#user/'+project.author.id" class="md-title"> {{ project.author.name }}</a>
          </div>
          <md-avatar class="md-avatar-icon md-warn">
            <md-icon>face</md-icon>
          </md-avatar>

          <md-card-actions>
            <md-button
              class="icon-text"
              @click.native="toggleSubscription(project.author)">
              <md-icon>visibility</md-icon> Watch
            </md-button>
          </md-card-actions>

        </div>
      </md-layout>

<!--       <md-card-actions>

        <span style="flex: 1;"></span>
        <md-button xclass="md-icon-button">
          <md-icon>star_border</md-icon> Bookmark
        </md-button>

        <md-button xclass="md-icon-button">
          <md-icon>thumb_up</md-icon> Like
        </md-button>
      </md-card-actions> -->

      <md-divider></md-divider>
      <md-card-content>
        
        <md-card class="subcard right">
          <p><label>Genres: </label> {{ project.genres.join(', ') }}</p>
          <p><label>Techniques: </label> {{ project.playing_styles.join(', ') }}</p>
          <p>
            <label>Tracks: </label>&nbsp;&nbsp;
            <img class="md-icon md-size-1x" src="../assets/drums.svg">
            <img class="md-icon md-size-1x" src="../assets/percussions.svg">
            <img class="md-icon md-size-1x" src="../assets/bass.svg">
            <img class="md-icon md-size-1x" src="../assets/piano.svg">
          </p>
        </md-card>

        <md-button class="md-primary md-raised open">
          OPEN
        </md-button>
        <br /><br />
        <p>
          Few words about the song/project
        </p>
      </md-card-content>
      <!-- <md-divider></md-divider> -->

    </md-card>
  </div>
</template>

<script>
  export default {
    name: 'detail',
    props: {
      project: Object,
      toggleLike: Function,
      toggleFavourite: Function,
      toggleSubscription: Function
    },
    components: {
      
    }
  }
</script>
<style lang="scss">
  .counter {
    padding: 0 3px;
  }
  .md-card.project {
    .header-section {
      background-color: #eee;
      flex: 1 0 auto;
      .md-card-actions {
        justify-content: flex-start;
        .md-button {
          padding-left: 4px;
        }
      }
    }
    .author-section {
      padding: 16px 0 0 16px;
      background-color: #eee;
      flex: 0 0 auto;
      .text {
        text-align: right;
        padding-top: 12px;
        display: inline-block;
        a {

        }
      }
      .md-avatar {
        float: right;
        width: 56px;
        height: 56px;
        margin: 8px 16px 12px 10px;
        .md-icon {
          width: 36px;
          height: 36px;
          font-size: 36px;
        }
      }
      .md-card-actions {
        width: 100%;
      }
    }
    .md-card-content {
      .md-icon {
        margin-right: 5px;
      }
      .video-link {
        float: right;
        font-size: 28px;
      }
      .subcard {
        float: right;
        min-width: 25%;
        padding: 6px 16px;
        margin: 6px 0 0 16px;
      }
      .md-button.open {
        padding: 0 70px;
        margin: 6px 0;
      }
    }
    label {
      font-weight: bold;
      color: #444;
      margin-right: 5px;
    }
  }
</style>