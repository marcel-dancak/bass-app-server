<template>
  <div class="page-container author-detail">
    <md-card class="author detail md-warn">
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

          <md-card-actions noauth-disable>
            <md-button
              class="icon-text"
              :class="{'md-primary': subscribed}"
              @click.native="toggleSubscribe(author)">
                <i class="fa fa-eye"></i> Subscribe
            </md-button>

            <div class="md-subhead">Uploads: {{ author.projects_count }}</div>
          </md-card-actions>
        </div>
        <div style="flex: 1"></div>
        <div class="right-section">
          <h4>Joined: {{ author.date_joined | todate }}</h4>
          <div class="icon-links">
            <md-button
              v-for="link in author.links"
              :href="link"
              target="_blank"
              class="md-icon-button">
              <i class="fa" :class="extractSite(link)"></i>
            </md-button>
          </div>
        </div>
      </md-layout>
    </md-card>

    <md-theme md-name="light">
      <responsive-list
        :projects="projects"
        showLastEdit>
        <md-button
          @click.native="$router.back"
          class="back md-icon-button">
          <md-icon>arrow_back</md-icon>
        </md-button>
        <h1 class="md-title">Projects</h1>
      </responsive-list>
    </md-theme>
  </div>
</template>

<script>
import ResponsiveList from './ResponsiveList'

export default {
  name: 'author-projects',
  components: {
    ResponsiveList
  },
  props: {
    id: [String, Number]
  },
  data () {
    return {
      author: {},
      query: '',
      projects: []
    }
  },
  computed: {
    subscribed() {
      return this.$store.state.user.subscribers.indexOf(this.author.id) !== -1
    }
  },
  created () {
    this.fetchProjects(this.$route.query)
  },
  watch: {
    '$route' (to, from) {
      if (to.name === 'author') {
        console.log('** AUTHOR PAGE **')
        this.fetchProjects(to.query)
      }
    }
  },
  methods: {
    fetchProjects(query) {
      console.log('fetching projects')
      this.$client.fetchUserProjects(this.id, query)
        .then(response => {
          this.projects = response.data.projects
          this.author = response.data.profile
        })
    },
    toggleSubscribe() {
      this.$client.toggleSubscribe(this.author)
    },
    extractSite(link) {
      const hostname = new URL(link).hostname
      const parts = hostname.split('.')
      let site = parts[parts.length-2]
      if (site === 'google' && parts[0] === 'plus') {
        site = 'google-plus'
      }
      return `fa-${site}-square`
    }
  }
}
</script>
<style lang="scss">

  .md-card.author {
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
      padding-top: 13px!important;
      padding-bottom: 8px!important;
      justify-content: flex-start;
      .md-button {
        padding-left: 8px;
      }
      .md-subhead {
        margin-left: 16px;
        opacity: 0.74;
        position: relative;
        padding-left: 14px;
        font-weight: 500;
        &:before {
          content: "";
          position: absolute;
          left: 0;
          top: 2px;
          bottom: 2px;
          width: 1px;
          background-color: #777;
        }
      }
    }
    .md-card-content {
      padding-bottom: 16px;
    }
    .right-section {
      margin: 16px 16px 10px 8px;
      text-align: right;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      h4 {
        opacity: 0.55;
        font-weight: 500;
      }
      .icon-links {
        margin-left: 16px;
        .md-button {
          padding: 4px;
          margin: 0;
          opacity: 0.7;
          &:hover {
            opacity: 0.9;
          }
        }
        i.fa {
          font-size: 28px;
          color: #fff;
        }
        .fa-patreon-square {
          background-image: url('../assets/patreon-square.svg');
          background-size: 24px;
          width: 24px;
          height: 24px;
          margin-top: 2px;
          xbackground-color: #e6461a;
          border-radius: 5px;
        }
      }
      .md-subhead {
        line-height: 30px;
        font-weight: 500;
      }
    }
  }
  </style>
  <style lang="scss">
  .author-detail {
    .md-list.projects {
      .author {
        visibility: hidden;
      }
      .rating:before {
        display: none;
      }
    }
    .md-toolbar {
      .back.md-button {
        margin-left: 0;
        margin-right: 0;
      }
    }
  }
  </style>