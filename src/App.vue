<template>
  <div class="container">
    <login-dialog ref="login" @login="onLogin"></login-dialog>
    <div class="page-wrapper">

      <md-sidenav
        ref="sidenav"
        class="main-sidebar md-left md-fixed">

          <md-card class="my-card md-accent">
            <md-card-header v-if="user.username">
              <md-card-header-text>
                <div class="md-title">
                  <router-link :to="{ path: '/profile' }">
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
            <md-divider></md-divider>
            <md-card-actions>
              <template v-if="user.username">
                <md-button @click.native="logout">
                  <md-icon>account_circle</md-icon> <span>Logout</span>
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
<!--             <template v-if="user.username">
              <md-list-item @click.native="logout">
                <md-icon>account_circle</md-icon> <span>Logout</span>
              </md-list-item>
            </template>
            <template v-else>
              <md-list-item @click.native="$refs.login.open">
                <md-icon>account_circle</md-icon> <span>Login</span>
              </md-list-item>
            </template>
            <md-divider></md-divider> -->

            <!-- My projects -->

            <md-list-item>
              <!-- <md-icon>fiber_new</md-icon> <span>New</span> -->
              <router-link :to="{ path: '/all'}">
                <md-icon>restore</md-icon> <span>All</span>
              </router-link>
            </md-list-item>
            <md-list-item>
              <router-link :to="{ path: '/favourite' }">
                <md-icon>start</md-icon> <span>Bookmarked</span>
              </router-link>
            </md-list-item>
            <md-list-item>
              <router-link :to="{ path: '/liked' }">
                <md-icon>thumb_up</md-icon> <span>Highest Rated</span>
              </router-link>
            </md-list-item>
          </md-list>
        </div>
      </md-sidenav>

      <transition :name="transition">
        <router-view @toggle-menu="$refs.sidenav.toggle()"></router-view>
      </transition>

    </div>
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
      user: this.$root.$data.user,
      projects: []
    }
  },
  components: {
    LoginDialog
  },
  created () {
    // setTimeout(this.getUserProfile, 1000)
    this.getUserProfile()
    this._historyStack = [this.$router.currentRoute.fullPath]
    let onResize = e => {
      const offset = Math.round(Math.max((window.innerWidth - 1600)/2, 0))
      document.body.style.transform = `translate3d(${offset}px, 0, 0)`
    }
    window.addEventListener('resize', onResize)
    onResize()
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
    getUserProfile() {
      this.$http.get('profile/')
        .then(response => {
          this.$root.updateUser(response.data)
          this.$forceUpdate()
          // this.$router.push({name: currentRoute.name, query: currentRoute.query})
          // this.$router.push({name: 'list'})
        })
    },
    onLogin(profile) {
      console.log('Login Successful')
      this.$root.updateUser(profile)
      this.$forceUpdate()
    },
    logout() {
      this.$http.get('logout/').then(response => {
        this.$router.go(0)
      })
    }
  }
}
</script>

<style lang="scss">
  @import 'variables.scss';
  @import 'animations.scss';

  $sizebar-size: 280px;

  .md-subhead {
    white-space:nowrap;
  }
  .r-pad {
    padding-right: 16px;
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
    xbox-shadow: none;
    .md-card-header {
      margin: 0;
      padding-bottom: 0;
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
  i.fa {
    font-size: 28px;
    line-height: 28px;
  }
  /*
  .active {
    color: #3f51b5;
  }*/
  .md-button.icon-text {
    min-width: 64px;
    i.md-icon {
      padding-bottom: 4px;
    }
    i.fa {
      font-size: 22px;
      vertical-align: middle;
      padding-bottom: 4px;
      width: 24px;
    }
    /*
    &.active .md-icon {
      color: #3f51b5;
    }*/
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
    @media (min-width: 1281px) {
      .menu.md-button {
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
    overflow: hidden;
  }

  body {
    max-width: 1600px;
  }
  @media (min-width: 1601px) {
    body {
      margin-right: auto;
      border-left: 1px solid #ccc;
      border-right: 1px solid #ccc;
    }
  }

  a:not(.md-button):hover {
    text-decoration: none!important;
  }
  .container {
    min-height: 100%;
    height: 100%;
    position: relative;
    display: flex;
    flex-flow: column nowrap;
    flex: 1;
    transition: $swift-ease-out;
    @media (min-width: 1281px) {
      padding-left: $sizebar-size;
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
      }
    }
  }

  .md-left.main-sidebar.md-sidenav {
    .md-sidenav-content {
      width: $sizebar-size;
      display: flex;
      flex-flow: column;
      overflow: hidden;
      @media (min-width: 1281px) {
        top: 0;
        pointer-events: auto;
        transform: translate3d(0, 0, 0)!important;
        box-shadow: $material-shadow-10dp;
        /* border-right: 1px solid #bbb; */
      }
    }
    .md-backdrop {
      @media (min-width: 1281px) {
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

  @media print {
    body {
      -webkit-print-color-adjust: exact;
    }
  }
  @page {
    size: 1740px 820px;
    margin: 0;
  }
</style>
