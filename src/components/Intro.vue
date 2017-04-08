<template>
  <div class="intro-page">
    <login-dialog ref="login" @login="afterLogin"></login-dialog>
    <div class="container">
      <header>
        <!-- <h1>BassCloud <img class="logo" src="../assets/logo.svg"></h1> -->
        <h1>
          <img class="text-logo" src="../assets/text_logo.svg">
          <img class="logo" src="../assets/logo.svg">
        </h1>
        <!-- <div>
          <img class="text_logo" src="../assets/text_logo.svg">
          <img class="logo" src="../assets/logo.svg">
        </div> -->
<!--         <router-link
          to="login"
          class="md-button md-theme-default md-primary md-raised">
          <span>Sign In</span>
        </router-link> -->
        <h4>Online platform for creating and sharing audio compositions wih focus on bass guitar</h4>

        <md-button v-if="!user.username"
          @click.native="$refs.login.open"
          class="md-primary md-raised">
          <span>Sign In</span>
        </md-button>

        <div v-else class="user">
          <div class="avatar">
            <md-avatar v-if="user.avatar">
              <img :src="$http.options.root+user.avatar">
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

      <hr />
      <br />

      <md-layout
        md-row md-column-small
        class="main-layout">
        <md-layout md-flex="45" md-column class="text-left">
          <h3>main goals</h3>
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
                <span class="md-title">Community of creators and followers</span>
                <p>
                  Provide mutually beneficial environment for authors and subscribers.
                  Give authors great tools for creating bass tracks in easy to learn form, and so motivate followers in rewarding them.
                </p>
              </div>
            </md-list-item>

            <md-list-item>
              <md-icon class="md-primary">trending_up</md-icon>
              <div class="md-list-text-container">
                <span class="md-title">Support for further development</span>
                <p>
                  Because <a href="http://marcel-dancak.github.io/drums-and-bass/">BassApp</a>
                  is a free and open source application, one of the BassCloud's service goals
                  is to provide financial support for its further development and maintenance.
                </p>
              </div>
            </md-list-item>

          </md-list>
        </md-layout>

        <div class="space"></div>

        <md-layout class="img-container" md-column>
          <img class="screenshot" src="../assets/app.svg">
          <br />
          <p>
            BassCloud is build as an extension service for the
            <a href="http://marcel-dancak.github.io/drums-and-bass/">BassApp</a>
            application, providing online storage space and catalog-like interface for projects created in it.
          </p>
        </md-layout>
      </md-layout>

      <hr />
      <div class="actions">
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
          <span>Create an account</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
  import LoginDialog from './Login'
  export default {
    name: 'intro',
    components: {
      LoginDialog
    },
    computed: {
      user() {
        return this.$store.state.user
      }
    },
    methods: {
      afterLogin () {
        this.$router.push({path: '/projects'})
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
  .intro-page {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    overflow: auto;
    xbackground-color: #f9f9f9;
    background-color: #fff;
    text-align: center;

    @media (min-width: 560px) {
      padding: 0 1em;
    }

    a:not(.md-button) {
      color: #2196f3;
    }

    .container {
      margin: 0 auto;
      max-width: 1240px;
      @media (max-width: 1280px) {
        padding: 0 16px;
      }
    }
    header {
      position: relative;
      .md-button {
        margin: auto 0;
        position: absolute;
        right: 0;
        top: 16px;
      }
      .user {
        position: absolute;
        right: 0;
        top: -2px;
        a {
          opacity: 0.85;
          font-size: 15px;
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
      margin-bottom: 16px;
    }
    .logo {
      width: 80px;
      margin-left: 28px;
    }
    .text-logo {
      margin-top: 10px;
      height: 42px;
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
    @media (max-width: 560px) {
      .logo {
        width: 64px;
      }
      .text-logo {
        height: 32px;
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
      .md-list-item {
        padding-bottom: 16px;
        max-width: 500px;
        .md-list-item-container {
          padding-left: 0!important;
        }
        .md-icon {
          margin-right: 24px;
        }
        @media (min-width: 560px) {
          &:nth-child(1) {
            padding-left: 0;
          }
          &:nth-child(2) {
            padding-left: 12px;
          }
          &:nth-child(3) {
            padding-left: 24px;
          }
        }
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
