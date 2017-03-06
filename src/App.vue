<template>
  <div class="container">
  <div style="position: relative;">
    <md-sidenav
      ref="sidenav"
      class="main-sidebar md-left md-fixed">
      <md-toolbar xclass="md-large">
        <div class="md-toolbar-container">
          <h3 class="md-title">Menu</h3>
        </div>
      </md-toolbar>

      <div class="main-sidebar-links">
        <md-list>
          <!-- My projects -->
          <!-- Most rated -->

          <md-list-item @click.native="filterNew">
            <!-- <md-icon>fiber_new</md-icon> <span>New</span> -->
            <md-icon>restore</md-icon> <span>New</span>
          </md-list-item>
          <md-list-item @click.native="filterFavourite">
            <md-icon>start</md-icon> <span>Favourite</span>
          </md-list-item>
          <md-list-item @click.native="filterFavourite">
            <md-icon>thumb_up</md-icon> <span>Most liked</span>
          </md-list-item>
          <md-divider></md-divider>
          <md-list-item @click.native="login">
            <md-icon>account_circle</md-icon> <span>Login</span>
          </md-list-item>
        </md-list>
      </div>
    </md-sidenav>

    <transition name="slide-fade-reverse">
      <div v-if="mode === 'list'">
        <md-toolbar class="md-warn main">
          <md-button class="menu md-icon-button" @click.native="$refs.sidenav.toggle()">
            <md-icon>menu</md-icon>
          </md-button>
          <h1 class="md-title">Catalog</h1>

          <div style="flex: 1"></div>

          <md-input-container style="flex: 1">
            <md-input
              type="text"
              placeholder="Search"
              v-model="query"
              @keyup.enter.native="search">
            </md-input>
          </md-input-container>

          <md-button
            class="md-icon-button"
            @click.native="search">
            <md-icon>search</md-icon>
          </md-button>
        </md-toolbar>

        <projects-list
          :projects="projects"
          :toggleFavourite="toggleFavourite">
        </projects-list>
        <!-- <projects-table :projects="projects"></projects-table> -->
      </div>
    </transition>
    <transition name="slide-fade">
      <detail
        v-if="mode === 'detail'"
        :project="selected"
        :toggleLike="toggleLike"
        :toggleFavourite="toggleFavourite"
        :toggleSubscription="toggleSubscription">
      </detail>
    </transition>

    <!-- <img src="./assets/logo.png"> -->
    <!-- <hello></hello> -->
    </div>
  </div>
</template>

<script>
import ProjectsList from './components/ProjectsList'
import ProjectsTable from './components/ProjectsTable'
import Detail from './components/Detail'

export default {
  name: 'app',
  components: {
    Detail,
    ProjectsList,
    ProjectsTable
  },
  data () {
    return {
      mode: 'list',
      query: '',
      user: null,
      projects: [],
      selected: {}
    }
  },
  created () {
    console.log('created')
    console.log(this.user)
    this.$http.post(
      'login/',
      {
        username: 'Marcel',
        password: 'qq'
      }
    ).then(response => {
      console.log('logged in')
      console.log(response.data)
      this.user = response.data
      this.search()
      this.route(location.hash.replace('#', ''))
    })
    window.addEventListener("hashchange", function(evt) {
      const hash = evt.newURL.split('#')[1]
      this.route(hash);
    }.bind(this))
  },
  methods: {
    route(hash) {
      if (hash && hash.startsWith('detail')) {
        this.mode = 'detail'
        const selectedId = hash.slice(7)
        console.log(hash)
        this.selected = this.projects.find((item) => {
          return item.id === selectedId
        }) || {}
      } else {
        this.mode = 'list'
      }
    },
    fetchProjects(query) {
      this.$http.get(
        'projects/',
        {
          params: query
        }
      ).then(response => {
            // get body data
            // let projects = 
            let projects = response.data;
            projects.forEach(function(item) {
              item.starred = this.user.favourites.indexOf(item.id) !== -1
              item.liked = this.user.likes.indexOf(item.id) !== -1
              item.author.subscribed = this.user.likes.indexOf(item.author.id) !== -1
            }, this)
            this.projects = projects
          }, response => {
            // error callback
        })
    },
    search(evt) {
      this.fetchProjects({
        q: this.query
      });
    },
    filterNew() {
      this.fetchProjects({});
    },
    filterFavourite() {
      this.fetchProjects({filter: 'favourite'});
    },
    toggleFavourite(project) {
      console.log('toggleFavourite')
      this.$http
        .post('star/', {project: project.id, value: !project.starred})
        .then(response => {
            project.starred = !project.starred
            if (project.starred) {
              this.user.favourites.push(project.id)
            } else {
              this.user.favourites.splice(this.user.favourites.indexOf(project.id), 1)
            }
          }, response => {

          })
    },
    toggleLike(project) {
      console.log('toggleLike')
      this.$http
        .post('like/', {project: project.id, value: !project.liked})
        .then(response => {
            project.liked = !project.liked
            if (project.liked) {
              this.user.likes.push(project.id)
              project.likes++
            } else {
              this.user.likes.splice(this.user.likes.indexOf(project.id), 1)
              project.likes--
            }
          }, response => {

          })
    },
    toggleSubscription(author) {
      console.log('toggle Subscription')
      this.$http
        .post('subscribe/', {author: author.id, value: !author.subscribed})
        .then(response => {
            author.subscribed = !author.subscribed
            
          }, response => {

          })
    }
  }
}
</script>

<style lang="scss">
  @import 'variables.scss';
  $sizebar-size: 280px;

/*
.active {
  color: #3f51b5;
}*/
.md-button.icon-text {
  i.md-icon {
    padding-bottom: 4px;
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
