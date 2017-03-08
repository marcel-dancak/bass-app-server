<template>
  <div class="container">
    <div style="position: relative;">

      <md-sidenav
        ref="sidenav"
        class="main-sidebar md-left md-fixed">

          <md-card class="my-card md-accent">
            <md-card-header>
              <md-card-header-text>
                <div class="md-title">{{ user.username }}</div>
                <div class="md-subhead">Full Name</div>
              </md-card-header-text>
              <md-card-media>
                <md-icon class="md-size-3x">face</md-icon>
              </md-card-media>
            </md-card-header>
          </md-card>

        <div class="main-sidebar-links">
          <md-list>
            <template v-if="user.username">
              <md-list-item @click.native="logout">
                <md-icon>account_circle</md-icon> <span>Logout</span>
              </md-list-item>
            </template>
            <template v-else>
              <md-list-item @click.native="login">
                <md-icon>account_circle</md-icon> <span>Login</span>
              </md-list-item>
            </template>
            <md-divider></md-divider>

            <!-- My projects -->

            <md-list-item>
              <!-- <md-icon>fiber_new</md-icon> <span>New</span> -->
              <router-link :to="{ path: '/all'}">
                <md-icon>restore</md-icon> <span>All</span>
              </router-link>
            </md-list-item>
            <md-list-item>
              <router-link :to="{ path: '/favourite' }">
                <md-icon>start</md-icon> <span>Favourite</span>
              </router-link>
            </md-list-item>
            <md-list-item>
              <router-link :to="{ path: '/liked' }">
                <md-icon>thumb_up</md-icon> <span>Most liked</span>
              </router-link>
            </md-list-item>
          </md-list>
        </div>
      </md-sidenav>

      <router-view @toggle-menu="$refs.sidenav.toggle()"></router-view>

      <login-dialog ref="login"></login-dialog>

    </div>
  </div>
</template>

<script>
import LoginDialog from './components/Login'

export default {
  name: 'app',
  data () {
    return {
      query: '',
      user: this.$root.$data.user,
      projects: []
    }
  },
  components: {
    LoginDialog
  },
  created () {
    setTimeout(this.getUserProfile, 1000)
    // this.getUserProfile()
  },
  methods: {
    updateUser(data) {
      Object.assign(this.$root.$data.user, data)
      Object.keys(this.$root.$data.user).forEach(function(key) {
        if (!data[key]) {
          delete this.$root.$data.user[key]
        }
      }, this)
    },
    getUserProfile() {
      this.$http.get('profile/')
        .then(response => {
          console.log('Profile')
          console.log(response.data)
          // this.$root.$data.user = response.data
          this.updateUser(response.data)
          // this.$router.push({name: currentRoute.name, query: currentRoute.query})
          // this.$router.push({name: 'list'})
        })
    },
    login() {
      this.$http.post(
        'login/',
        {
          username: 'Marcel',
          password: 'qq'
        }
      ).then(response => {
        console.log('logged in')
        this.$root.$data.user = response.data
      }, response => {
        console.log('failed to login')
      })
    },
    logout() {
      this.$refs.login.open()
      return
      this.$http.get('logout/').then(response => {
        this.$router.go(0)
      })
    }
  }
}
</script>

<style lang="scss">
  @import 'variables.scss';
  $sizebar-size: 280px;

.r-pad {
  padding-right: 16px;
}
.my-card.md-card {
  border-radius: 0;
  background-color: red;
  .md-card-header {
    margin: 0;
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

.slide-fade-enter-active {
  transition: all .45s ease;
  position: absolute;
  width: 100%;
  top: 0;
}
.slide-fade-leave-active {
  transition: all .45s linear;
  position: absolute;
  width: 100%;
  top: 0;
}
.slide-fade-enter, .slide-fade-leave-to {
  transform: translateX(300px);
  opacity: 0;
}

.slide-fade-reverse-enter-active {
  transition: all .35s ease;
}
.slide-fade-reverse-leave-active {
  transition: all .45s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-reverse-enter, .slide-fade-reverse-leave-to {
  transform: translateX(-300px);
  opacity: 0;
}

.md-card {
  xbackground-color: red!important;
}

  .md-toolbar.main {
    .md-input-container {
      margin-bottom: 12px;
    }
    .md-input-container {
      max-width: 300px;
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
    display: flex;
  }
  a:not(.md-button):hover {
    text-decoration: none!important;
  }
  .container {
    min-height: 100%;
    display: flex;
    flex-flow: column nowrap;
    flex: 1;
    transition: $swift-ease-out;
    @media (min-width: 1281px) {
      padding-left: $sizebar-size;
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
        box-shadow: $material-shadow-2dp;
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
</style>
