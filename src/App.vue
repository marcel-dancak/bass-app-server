<template>
  <div class="app-container" :class="[user.username? 'auth' : 'noauth']">
    <div class="app">
      <login-dialog ref="login"></login-dialog>
      <div class="page-wrapper">

        <transition :name="transition">
          <keep-alive include="list,author-projects">
            <router-view @toggle-menu="$refs.sidenav.toggle()"></router-view>
          </keep-alive>
        </transition>

      </div>
    </div>

    <md-sidenav
      ref="sidenav"
      class="main-sidebar md-left"
      @click.native="afterClick">
        <md-card class="my-card md-accent">
          <md-card-header v-if="user.username">
            <md-card-header-text>
              <div class="md-title">
                <router-link to="/profile">
                  {{ user.username }}
                </router-link>
              </div>
              <div class="md-subhead">{{ user.first_name}} {{ user.last_name }}</a></div>
            </md-card-header-text>
            <md-card-media>
              <md-avatar v-if="user.avatar" class="md-large">
                <img :src="$http.options.root+user.avatar">
              </md-avatar>
              <!-- <img class="md-avatar" v-if="user.avatar" :src="user.avatar"> -->
              <md-icon v-else class="md-size-3x">face</md-icon>
            </md-card-media>
          </md-card-header>
          <md-card-header v-else class="logo">
            <img src="./assets/logo-dark.svg">
            <!-- <router-link
              class="register-link"
              :to="{ name: 'registration' }">Create Account
            </router-link> -->
          </md-card-header>

          <md-divider></md-divider>
          <md-card-actions>
            <template v-if="user.username">
              <md-button @click.native="logout">
                <md-icon>power_settings_new</md-icon>
                <!-- <md-icon>account_circle</md-icon> -->
                <span>Logout</span>
              </md-button>
            </template>
            <template v-else>
              <md-button @click.native="$refs.login.open">
                <md-icon>account_circle</md-icon> <span>Login</span>
              </md-button>
            </template>
          </md-card-actions>
        </md-card>

      <div class="main-sidebar-links">
        <md-list>

          <md-subheader>Projects</md-subheader>
          <md-list-item>
            <!-- <md-icon>fiber_new</md-icon> <span>New</span> -->
            <router-link :to="{ path: '/projects', query: $route.query}" exact>
              <md-icon>restore</md-icon>
              <span>All Projects</span>
            </router-link>
          </md-list-item>

          <md-list-item v-if="user.projectsCount">
            <router-link :to="{ path: '/created', query: $route.query }">
              <md-icon>create</md-icon>
              <span>My Projects</span>
            </router-link>
          </md-list-item>

          <md-list-item noauth-hide>
            <router-link :to="{ path: '/bookmarked', query: $route.query }">
              <md-icon>start</md-icon>
              <span>Bookmarked</span>
            </router-link>
          </md-list-item>

          <md-list-item noauth-hide>
            <router-link :to="{ path: '/subscribed', query: $route.query }">
              <md-icon>visibility</md-icon>
              <span>Subscribed</span>
            </router-link>
          </md-list-item>

          <!-- <md-divider></md-divider> -->
          <md-subheader>Links</md-subheader>
          <md-list-item href="/app" target="_blank">
            <!-- exit_to_app, queue_play_next, web, computer -->
            <md-icon>queue_play_next</md-icon>
            <span>BassApp</span>
          </md-list-item>
          <md-list-item>
            <router-link to="/" exact>
              <md-icon>home</md-icon>
              <span>Home Page</span>
            </router-link>
          </md-list-item>
          <md-list-item auth-hide>
            <router-link :to="{ name: 'registration' }">
              <!-- <md-icon>account_box</md-icon> -->
              <!-- <md-icon>assignment_ind</md-icon> -->
              <md-icon>person_add</md-icon>
              <span>Create Account</span>
            </router-link>
          </md-list-item>
        </md-list>
      </div>
    </md-sidenav>
  </div>
</template>

<script>
import LoginDialog from './components/Login'

export default {
  name: 'app',
  data () {
    return {
      transition: 'slide',
      query: '',
      projects: []
    }
  },
  computed: {
    user() {
      return this.$store.state.user
    }
  },
  components: {
    LoginDialog
  },
  created () {
    this._historyStack = [this.$route.fullPath]
  },
  watch: {
    '$route' (to, from) {
      const toDepth = to.path.split('/').length
      const fromDepth = from.path.split('/').length
      // console.log('Current: '+to.fullPath)
      // console.log(this._historyStack)
      if (history.length <= this._historyDepth && to.fullPath === this._historyStack[this._historyStack.length-2]) {
        // console.log('BACK')
        this._historyStack.pop()
        this._historyStack.pop()
        this.transition = 'slide-inverse'
      } else {
        // console.log('FORWARD')
        this.transition = 'slide'
      }
      // this.transition = toDepth < fromDepth ? 'slide-inverse' : 'slide'
      this._historyDepth = history.length
      this._historyStack.push(to.fullPath)
      // console.log(this._historyStack)
    }
  },
  methods: {
    logout() {
      this.$http.get('logout/').then(response => {
        this.$router.go(0)
        // this.$router.replace({path: '/'}, e => {location.reload()})
      })
    },
    afterClick(evt) {
      if (window.innerWidth < 1280) {
        this.$refs.sidenav.close()
      }
    }
  }
}
</script>

<style lang="scss">
  @import 'variables.scss';
  @import 'animations.scss';
  @import 'base.scss';

  $fa-font-path: "~font-awesome/fonts";
  @import "~font-awesome/scss/font-awesome.scss";

  $sizebar-size: 280px;

  .md-chips.with-label {
    padding-top: 6px;
    label {
      top: -10px;
      opacity: 1;
    }
  }

  .md-card.md-accent, .md-card.md-warn {
    a:not(.md-button) {
      color: #eee;
      &:hover {
        color: #fff;
      }
    }
  }
  .my-card.md-card {
    border-radius: 0;
    border-right: 1px solid #666;
    overflow: hidden;
    .md-card-header {
      margin: 0;
      padding-bottom: 0;
      /* fix for transition animation (destroyed() which
        removes flex layout is called before transition ends) */
      display: flex;

      &.logo {
        xflex-direction: column;
        xpadding-top: 4px;
        opacity: 0.8;
        height: 96px;
        img {
          margin-top: 6px;
          height: 48px;
          object-position: 0 0;
          object-fit: contain;
        }
        .register-link {
          padding: 14px 0 10px 24px;
        }
      }
    }
    .md-card-actions {
      padding: 6px;
      justify-content: flex-start;
      .md-button {
        padding: 0 10px;
        text-transform: none;
        width: 100%;
        text-align: left;
      }
      .md-icon {
        margin-right: 26px;
      }
    }
    .md-divider {
      margin: 0 8px;
      /*opacity: 0.55;*/
    }
  }

  .md-toolbar.main {
    h1 {
      padding-left: 8px;
      padding-right: 16px;
    }
    .md-input-container {
      margin-left: auto;
      margin-bottom: 12px;
      max-width: 360px;
      padding-top: 15px;
    }
    .menu.md-button {
      margin-right: 0;
      @media (min-width: 1280px) {
        display: none;
      }
    }
  }

  [v-cloak] {
    display: none;
  }

  html,
  body {
    height: 100%;
    width: 100%;
    overflow: hidden;
    xdisplay: flex;
    xjustify-content: center;
  }

  .page-wrapper {
    position: relative;
    min-height: 100%;
    height: 100%;
    .page-container {
      position: absolute;
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      background-color: #fff;
      overflow: auto;
      display: flex;
      flex-direction: column;
    }
  }

  .app-container {
    max-width: 1600px;
    min-height: 100%;
    height: 100%;
    position: relative;
    margin: 0 auto;
    xflex: 1;

    &.noauth {
      .noauth-disable, [noauth-disable] {
        opacity: 0.5;
        pointer-events: none;
      }
      .noauth-hide, [noauth-hide] {
        display: none;
      }
    }
    &.auth {
      .auth-hide, [auth-hide] {
        display: none;
      }
    }
  }
  @media (min-width: 1601px) {
    .app-container {
      border-right: 1px solid #ccc;
    }
  }

  a:not(.md-button):hover {
    text-decoration: none!important;
  }

  /* Remove yellow background from 'remembered' input fields */
  form input:-webkit-autofill {
    -webkit-box-shadow: 0 0 0px 1000px #fff inset;
    /* -webkit-text-fill-color: #000; */
  }
  .app {
    min-height: 100%;
    height: 100%;
    position: relative;
    display: flex;
    flex-flow: column nowrap;
    flex: 1;
    transition: $swift-ease-out;
    @media (min-width: 1280px) {
      padding-left: $sizebar-size;
    }
  }

  .md-left.main-sidebar.md-sidenav {
    .md-sidenav-content {
      width: $sizebar-size;
      display: flex;
      flex-flow: column;
      overflow: hidden;
      @media (min-width: 1280px) {
        top: 0;
        pointer-events: auto;
        transform: translate3d(0, 0, 0)!important;
        box-shadow: $material-shadow-10dp;
        /* border-right: 1px solid #bbb; */
      }
    }
    .md-backdrop {
      @media (min-width: 1280px) {
        opacity: 0;
        pointer-events: none;
      }
    }

    .main-sidebar-links {
      overflow: auto;
      flex: 1;
      border-right: 1px solid #bbb;
      .md-inset .md-list-item-container {
        padding-left: 36px;
      }
      .md-list-item-container {
        font-size: 14px;
        font-weight: 500;
      }
      .md-subheader {
        font-size: 12px;
        min-height: 36px;
        height: 36px;
        line-height: 42px;
        vertical-align: bottom;
        display: block;
        opacity: 0.5;
      }
    }
  }

  .main-content {
    padding: 16px;
    flex: 1;
    overflow: auto;
    background-color: #fff;
    transform: translate3D(0, 0, 0);
    transition: $swift-ease-out;
    transition-delay: .2s;
  }

</style>
