<template>
  <div class="intro-page">
    <login-dialog ref="login" @login="afterLogin"></login-dialog>
    <feedback-dialog ref="feedback" @sent="afterFeedback"></feedback-dialog>
    <div class="container">
      <div class="header-container">
        <div class="label"><span>Test version</span></div>
        <header>
          <img class="logo" src="../assets/logo2.svg">
          <h4>Online platform for creating and sharing audio compositions wih primary focus on the bass guitar</h4>

          <md-button v-if="!user.username"
            @click.native="$refs.login.open"
            class="md-primary md-raised">
            <span>Sign In</span>
          </md-button>

          <div v-else class="user">
            <div class="avatar">
              <md-avatar v-if="user.avatar">
                <img :src="$http.options.media+user.avatar">
              </md-avatar>
              <md-icon v-else class="md-size-2x">face</md-icon>
            </div>
            <router-link to="/profile">{{ user.username }}</router-link>
          </div>
  <!--         <md-button v-else
            @click.native="$router.push('projects')"
            class="md-primary md-raised">
            <span>Sign Out</span>
          </md-button> -->

        </header>
      </div>

      <br />

      <md-layout
        md-row md-column-small
        class="main-layout content">
        <md-layout md-flex="45" md-column class="text-left">
          <h3>It would be nice to achieve</h3>
          <br />
          <md-list>

            <md-list-item>
              <md-icon class="md-primary">queue_music</md-icon>
              <div class="md-list-text-container">
                <span class="md-title">Rich collection of basselines</span>
                <p>
                  Aim is to collect wide range of bass material (covers, lessons, excercises)
                  with all kinds of musical genres, playing styles and difficulty levels.
                </p>
              </div>
            </md-list-item>

            <md-list-item>
              <md-icon class="md-primary">share</md-icon>
              <div class="md-list-text-container">
                <span class="md-title">Strong community of users</span>
                <p>
                  Find some skilled authors and keep them motivated for regular uploading of new projects.
                  On the other side, there should be sufficient amount end users supporting this project.
                </p>
              </div>
            </md-list-item>

            <md-list-item>
              <md-icon class="md-primary">trending_up</md-icon>
              <div class="md-list-text-container">
                <span class="md-title">Support for further development</span>
                <p>
                  Because <a href="http://marcel-dancak.github.io/bass-app/">BassApp</a>
                  is a free and open source application, one of the BassCloud's goals
                  is to provide financial support for its further development and maintenance.
                </p>
              </div>
            </md-list-item>

          </md-list>
        </md-layout>

        <div class="space"></div>

        <md-layout class="img-container" md-column>
          <a href="/app"><img class="screenshot" src="../assets/app.svg"></a>
          <br />
          <p>
            BassCloud is build as an extension service for the
            <a href="http://marcel-dancak.github.io/bass-app/">BassApp</a>
            application, providing online storage space and interactive catalog interface for projects created in it.
          </p>
        </md-layout>
      </md-layout>

      <div class="actions">
        <hr style="margin: 0 0 16px 0"/>
        <router-link
          to="projects"
          :class="{'md-primary': user.username}"
          class="md-button md-raised md-theme-default">
          <span>Continue</span>
        </router-link>

        <router-link
          to="registration"
          :class="{'md-primary': !user.username}"
          class="md-button md-raised md-theme-default">
          <span>Create account</span>
        </router-link>
      </div>
      <div style="flex:1"></div>
      <footer>
        &nbsp;&nbsp;&nbsp;&nbsp;
        <!-- <md-icon class="xmd-size-2x">info</md-icon> -->
        <a class="md-button" href="http://marcel-dancak.github.io/bass-app/">
          <!-- <md-icon class="small">info</md-icon> -->
          <img class="logo" src="../assets/bassapp_logo.svg">
        </a>
        <md-button @click.native="$refs.feedback.open">
          <md-icon>message</md-icon>
          Feedback
        </md-button>
      </footer>
    </div>
    <md-snackbar
      ref="snackbar"
      md-position="bottom right"
      md-duration="3000">
      <span>Your feedback was successfully sent.</span>
    </md-snackbar>
  </div>
</template>

<script>
  import LoginDialog from './Login'
  import FeedbackDialog from './Feedback'

  export default {
    name: 'intro',
    components: {
      LoginDialog,
      FeedbackDialog
    },
    computed: {
      user() {
        return this.$store.state.user
      }
    },
    methods: {
      afterLogin () {
        this.$router.push({path: '/projects'})
      },
      afterFeedback () {
        this.$refs.snackbar.open()
      }
    }
  }
</script>

<style lang="scss" scoped>
  .align-right {
    margin-left: auto;
    margin-right: 0;
  }
</style>

<style lang="scss">
  @import '../variables.scss';

  .intro-page {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    overflow: auto;
    background-color: #f9f9f9;
    text-align: center;

    a:not(.md-button) {
      color: #2196f3;
    }
    .container {
      min-height: 100%;
      width: 100%;
      display: flex;
      flex-direction: column;

      header, .content, .actions {
        max-width: 1240px;
        margin: 0 auto;
        width: 100%;
        padding-left: 16px;
        padding-right: 16px;
        @media (min-width: 1280px) {
          width: 1240px;
        }
      }
      .header-container {
        padding-top: 10px;
        background-color: #607D8B;

        .label {
          color: #fff;
          font-weight: 500;
          position: absolute;
          text-align: center;

          transform: rotate(-35deg);
          box-shadow: $material-shadow-3dp;

          top: 0px;
          left: -38px;
          width: 136px;
          height: 44px;
          line-height: 18px;
          font-size: 13px;
          /*background-color: #EEEEEE;*/
          background-color: #FFC400;
          color: #616161;
          opacity: 0.75;

          span {
            padding-top: 3px;
            display: table-cell;
            vertical-align: middle;
            word-spacing: 120px;
          }
        }
      }
    }
    footer {
      height: 52px;
      margin-top: 20px;
      background-color: #B0BEC5;
      color: #444;
      line-height: 52px;
      .md-icon {
        width: 32px;
        height: 32px;
        font-size: 32px;
        &.small {
          width: 26px;
          font-size: 24px;
        }
      }
      .logo {
        height: 17px;
      }
    }
    header {
      padding-top: 16px;
      position: relative;
      color: #fff;
      .logo {
        height: 58px;
      }
      .md-button {
        margin: auto 0;
        position: absolute;
        right: 16px;
        top: 16px;
      }
      .user {
        position: absolute;
        right: 0;
        top: 8px;
        a {
          opacity: 0.55;
          font-size: 15px;
          color: #fff;
          &:hover {
            color: #fff;
            opacity: 0.75;
          }
        }
        .avatar {
          xdisplay: inline-block;
          .md-avatar {
            width: 50px;
            height: 50px;
          }
        }
      }
      h1 {
        height: 72px;
        line-height: 80px;
        img {
          transform: translateY(-12px);
        }
      }
      @media (max-width: 600px) {
        /*
        h1 {
          text-align: left;
          img {
            float: right;
          }
        }*/
        .md-button {
          position: static;
          margin-bottom: 24px;
        }
        .user {
          display: none;
        }
      }
    }
    h1 {
      opacity: 0.85;
    }
    h4 {
      font-size: 17px;
      opacity: 0.85;
      font-weight: 500;
    }
    h3 {
      text-transform: uppercase;
      font-size: 20px;
    }
    hr {
      opacity: 0.4;
    }

    .subheader {
      padding-top: 2px;
      font-size: 17px;
      font-weight: 500;
      opacity: 0.55;
      padding-right: 34px;
      xpadding-right: 96px;
    }
    .img-container {
      width: 630px;
      max-width: 100%;
      margin-left: auto;
      margin-right: auto;
      p {
        color: rgba(0,0,0,.54);
      }
    }
    .screenshot {
      -webkit-filter: drop-shadow(1px 2px 4px #333);
      filter: drop-shadow(1px 2px 4px #555);
    }
    .main-layout {
      flex-wrap: nowrap;
      min-height: 50vh;
      a {
        font-weight: 500;
      }
      .space {
        width: 24px;
        height: 24px;
      }
      > .md-layout {
        margin-top: auto;
        margin-bottom: auto;
        flex-wrap: nowrap;
      }
    }
    .md-list {
      background-color: transparent!important;
      .md-list-item {
        padding-bottom: 16px;
        max-width: 500px;
        .md-list-item-container {
          padding-left: 0!important;
        }
        .md-icon {
          margin-right: 24px;
        }
        /*
        @media (min-width: 1280px) {
          &:nth-child(2) {
            padding-left: 12px;
          }
        } */
      }
      .md-title {
        text-transform: uppercase;
      }
      p {
        white-space: normal;
      }
    }
    .actions {
      .md-button {
        min-width: 180px;
      }
    }
  }

</style>
