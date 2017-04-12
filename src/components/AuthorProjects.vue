<template>
  <div class="page-container author-detail">
    <md-card class="author detail md-warn">
      <md-card-header>
        <md-layout md-row>
          <img
            v-if="author.avatar"
            class="md-avatar avatar"
            :src="$http.options.root+author.avatar">
          <md-icon v-else class="avatar">face</md-icon>
          <md-card-header-text>
            <div class="md-title">{{ author.username }}</div>
            <div class="md-subhead">{{ author.first_name }} {{ author.last_name }}</div>
            <span class="date md-subhead md-hide-xsmall">Joined: {{ author.date_joined | todate }}</span>
          </md-card-header-text>
          <!-- <p class="md-flex text-right">
            <span class="md-subhead">Joined: {{ author.date_joined | todate }}</span>
          </p> -->
        </md-layout>
      </md-card-header>

      <md-card-actions>
        <md-button
          noauth-disable
          class="icon-text"
          :class="{'md-primary': subscribed}"
          @click.native="toggleSubscribe(author)">
            <i class="fa fa-eye"></i> &nbsp;Subscribe
            <small v-if="author.subscribers_count">&nbsp;/ {{ author.subscribers_count }}</small>
        </md-button>

        <div class="md-subhead">Uploads: {{ author.projects_count }}</div>
        <div style="flex: 1"></div>

        <md-button
          v-for="link in author.links"
          :href="link"
          target="_blank"
          class="md-icon-button">
          <i class="fa" :class="extractSite(link)"></i>
        </md-button>
      </md-card-actions>
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

  .fa-patreon-square {
    background-image: url('../assets/patreon-square.svg');
    background-size: 24px;
    width: 24px;
    height: 24px;
    margin: 2px 0;
    xbackground-color: #e6461a;
    border-radius: 5px;
  }

  .md-card.author {
    box-shadow: none;
    border-radius: 0;

    .md-card-header {
      padding-bottom: 6px;
      .avatar {
        margin-left: 0;
        margin-right: 10px;
        width: 72px;
        height: 72px;
        font-size: 72px;
        flex: 0 0 auto;
      }
      .md-card-header-text {
        margin-top: 8px;
        position: relative;
        .date {
          position: absolute;
          right: 0;
          top: 16px;
        }
      }
    }
    .md-card-actions {
      justify-content: flex-start;
      height: 52px;
      .md-button.icon-text {
        padding-left: 8px;
        min-width: 112px;
      }
      .md-subhead {
        margin-left: 16px;
        margin-right: 12px;
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

    .md-button.md-icon-button {
      padding: 4px;
      margin: 0;
      opacity: 0.7;
      display: inline;
      &:hover {
        opacity: 0.9;
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