<template>
  <div class="page-container">
    <md-toolbar class="md-warn main">
      <h1 class="md-title">Profile</h1>
    </md-toolbar>
    <form class="profile-form">
      <md-input-container>
        <label>Username</label>
        <md-input v-model="form.username" disabled></md-input>
      </md-input-container>

      <md-input-container>
        <label>Profile Photo</label>
        <md-file
          v-model="form.avatar"
          accept="image/*"
          name="avatar">
        </md-file>
      </md-input-container>

      <md-input-container>
        <label>First Name</label>
        <md-input
          name="first_name"
          v-model="form.first_name">
        </md-input>
      </md-input-container>

      <md-input-container>
        <label>Last Name</label>
        <md-input
          name="last_name"
          v-model="form.last_name">
        </md-input>
      </md-input-container>

      <md-input-container>
        <label>E-mail</label>
        <md-input
          name="email"
          type="email"
          required
          v-model="form.email">
        </md-input>
      </md-input-container>

      <md-chips
        v-chips-label="'Links'"
        v-model="form.links"
        :md-max="6"
        class="with-label"
        md-input-placeholder="Add profile link (Youtube, Facebook, Patreon, ...)">
        <!-- :md-input-placeholder="form.links && form.links.length? 'Add' : 'External profiles (Youtube, Facebook, Patreon, ...)'"> -->
        <template scope="chip">{{ chip.value }}</template>
      </md-chips>
      <input name="links" type="hidden" v-model="links">

    <md-toolbar class="md-warn main md-transparent">
      <div style="flex:1"></div>
      <md-button
        class="md-raised"
        @click.native="back">
        Cancel
      </md-button>
      <md-button
        class="md-raised md-primary"
        @click.native="save">
        Save
      </md-button>
    </md-toolbar>

    </form>
  </div>
</template>

<script>

export default {
  name: 'user-profile',
  data () {
    return {
      form: {},
    }
  },

  computed: {
    user() {
      return this.$store.state.user
    },
    links() {
      return this.form.links? this.form.links.join(',') : ''
    }
  },
  created () {
    if (this.user.username) {
      this.initializeForm()
    }
  },
  watch: {
    user (newVal, oldVal) {
      console.log('user changed')
      this.initializeForm()
    }
  },
  methods: {
    back() {
      this.$router.go(-1)
    },
    initializeForm() {
      let form = {}
      const fields = ['id', 'username', 'first_name', 'last_name', 'email', 'links']
      fields.forEach(key => {
          form[key] = this.user[key]
        })
    this.form = form
    },
    save() {
      var formData = new FormData(this.$el.querySelector('form'));
      this.$http.post(
        'profile/',
        formData
      ).then(response => {
        this.$store.commit('updateProfile', response.data)
        this.$router.back()
      })
    }
  }
}
</script>
<style lang="scss">

  .profile-form {
    padding: 16px;
    max-width: 600px;
    .md-chip {
      width: 100%;
    }
  }
</style>