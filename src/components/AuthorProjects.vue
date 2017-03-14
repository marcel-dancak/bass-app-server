<template>
  <div>
    <md-card class="author detail">
      <md-layout>
        <div class="main-section">
          <md-card-header>
            <img
              v-if="author.avatar"
              class="md-avatar avatar"
              :src="$http.options.root+author.avatar">
            <md-icon v-else class="avatar">face</md-icon>
            <md-card-header-text>
              <div class="md-title">{{ author.username }}</div>
              <div class="md-subhead">{{ author.first_name }} {{ author.last_name }}</div>
            </md-card-header-text>
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

            <!-- <div class="md-subhead">Joined: {{ author.date_joined | todate }}</div> -->
          </md-card-actions>
        </div>
        <div style="flex: 1"></div>
        <div class="right-section">
          <h4>Joined: {{ author.date_joined | todate }}</h4>
          <h3>Uploads: {{ author.projects_count }}</h3>
          <!-- <div class="md-subhead">Uploads: {{ author.projects_count }}</div> -->
        </div>
      </md-layout>

      <md-toolbar class="main xmd-transparent">
        <md-button
          @click.native="back"
          class="back md-icon-button xmd-raised">
          <md-icon>arrow_back</md-icon>
        </md-button>
          <h2 class="md-title">Projects</h2>

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
    box-shadow: none;
    border-radius: 0;

    .md-card-header {
      padding-bottom: 0;
      justify-content: flex-start;
      flex-direction: row;
      display: flex;
      .avatar {
        margin-left: 0;
        margin-right: 10px;
        width: 72px;
        height: 72px;
        font-size: 72px;
        flex: 0 0 auto;
      }
      .md-card-header-text {
        flex: 0;
      }
    }
    .md-card-actions {
      padding-top: 12px!important;
      padding-bottom: 4px!important;
      .md-button {
        padding-left: 8px;
      }
      .icon-links {
        margin-left: 16px;
        padding-left: 8px;
        position: relative;
        &:before {
          content: "";
          position: absolute;
          left: 0;
          top: 6px;
          bottom: 6px;
          width: 1px;
          background-color: #bbb;
        }
        .md-button {
          padding: 4px;
        }
        i {
          font-size: 24px;
          color: #333;
        }
      }
    }
    .md-card-content {
      padding-bottom: 16px;
      background-color: #fff;
    }
    .right-section {
      margin: 16px 16px 0px 8px;
      text-align: right;
      display: flex;
      flex-direction: column;
      xjustify-content: flex-end;
      justify-content: space-between;
      h4 {
        color: #777;
        font-weight: 500;
      }
      h3 {
        margin: 12px 0;
        color: #444;
      }
      .md-subhead {
        line-height: 30px;
        font-weight: 500;
      }
    }
    .md-toolbar {
      background-color: #A1887F;
      /*
      background-color: #fff!important;
      border-top: 1px solid rgba(180,180,180,0.45);
      border-bottom: 1px solid #ccc;
      opacity: 0.75;
      */
      .back.md-button {
        margin-left: 4px;
        margin-right: 12px;
      }
    }
  }
</style>