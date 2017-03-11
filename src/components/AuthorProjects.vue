<template>
  <!-- <transition name="slide-fade-reverse"> -->
    <div>
      <md-card class="author detail">

        <md-card-header>
          <md-icon class="avatar">face</md-icon>
          <md-card-header-text>
            <div class="md-title">{{ author.username }}</div>
            <div class="md-subhead">Full Name</div>
          </md-card-header-text>
          <div style="flex: 1"></div>
<!--           <md-card-header-text>
            <div class="md-title">&nbsp</div>
            <div class="md-subhead" style="white-space:nowrap">Joined: {{ author.date_joined }}</div>
          </md-card-header-text> -->
          <div class="icon-links">
            <md-button href="#" class="md-icon-button">
              <i class="fa fa-youtube"></i>
            </md-button>
            <md-button href="#" class="md-icon-button">
              <i class="fa fa-facebook"></i>
            </md-button>
            <md-button href="#" class="md-icon-button">
              <i class="fa fa-twitter"></i>
            </md-button>
          </div>
        </md-card-header>

        <md-card-actions>
          <md-button
            class="icon-text"
            @click.native="toggleSubscription(project.author)">
              <i
                class="fa"
                :class="[subscribed? 'fa-eye-slash' : 'fa-eye']">
              </i>
              Subscribe
          </md-button>
          <div style="flex: 1"></div>
          <div class="md-subhead" style="white-space:nowrap">Joined: {{ author.date_joined }}</div>

<!--           <md-button href="#" class="md-icon-button">
            <i class="fa fa-youtube"></i>
          </md-button>
          <md-button href="#" class="md-icon-button">
            <i class="fa fa-facebook"></i>
          </md-button>
          <md-button href="#" class="md-icon-button">
            <i class="fa fa-twitter"></i>
          </md-button> -->
          <span>&nbsp;</span>
        </md-card-actions>

    <md-toolbar class="main xmd-transparent">
      <md-button
        @click.native="back"
        class="back md-icon-button xmd-raised">
        <md-icon>arrow_back</md-icon>
      </md-button>
        <h1 class="md-title">Projects</h1>

        <md-input-container style="flex: 1 0">
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

<!--         <md-layout md-row md-column-xsmall>
          <md-layout md-row class="actions-toolbar md-toolbar main">
            <md-button 
              @click.native="back"
              class="back md-icon-button md-fab md-raised md-clean">
              <md-icon>arrow_back</md-icon>
            </md-button>
            <h1>Projects</h1>

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
          </md-layout>
        </md-layout> -->

      </md-card>
      
      <projects-list :projects="projects"></projects-list>
      <!-- <projects-table :projects="projects"></projects-table> -->

    </div>
  <!-- </transition> -->
</template>

<script>
import ProjectsList from './ProjectsList'
import ProjectsTable from './ProjectsTable'

export default {
  name: 'author-projects',
  components: {
    ProjectsList,
    ProjectsTable
  },
  props: {
    q: String,
    id: [String, Number]
  },
  data () {
    return {
      author: {},
      subscribed: true,
      query: '',
      projects: [],
    }
  },
  created () {
    this.query = this.q
    this.fetchProjects(this.query)
  },
  methods: {
    back() {
      this.$router.go(-1)
    },
    fetchProjects(query) {
      console.log('fetching projects')
      this.$http.get(
        `projects/author/${this.id}`,
        {params: query}
      ).then(response => {
          // get body data
          let projects = response.data.projects
          let user = this.$root.$data.user

          projects.forEach(function(item) {
            item.starred = user.favourites.indexOf(item.id) !== -1
            item.liked = user.likes.indexOf(item.id) !== -1
          }, this)
          this.projects = projects
          this.$root.$data.projects = projects
          this.author = response.data.profile
          this.author.date_joined = new Date(this.author.date_joined).toLocaleDateString()
          console.log(this.author)
        }, response => {
          // error callback
        })
    },
    search() {
      this.fetchProjects({q: this.query})
    },
    toggleMenu() {
      this.$emit('toggle-menu')
    }
  }
}
</script>
<style lang="scss">
  .md-card.author {
    background-color: #FFF9C4!important;
    xbackground-color: #8D6E63!important;

    .md-card-header {
      padding-bottom: 0;
      justify-content: flex-start;
      flex-direction: row;
      display: flex;
      .avatar {
        margin-left: 0;
        margin-right: 8px;
        width: 72px;
        height: 72px;
        font-size: 72px;
        flex: 0 0 auto;
      }
      .md-card-header-text {
        flex: 0;
      }
      .icon-links {
        flex: 1;
        margin-top: 14px;
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
      }
    }
    .md-card-actions {
      padding: 10px 8px!important;
    }
    .md-card-content {
      padding-bottom: 16px;
      background-color: #fff;
    }
    .md-toolbar {
      background-color: #A1887F;
      xackground-color: #eee!important;
      .back.md-button {
        margin-left: 4px;
        margin-right: 12px;
      }
    }
  }
</style>