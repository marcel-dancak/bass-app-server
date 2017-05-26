<template>
  <div class="page-container">
    <md-toolbar class="md-warn main">
      <h1 class="md-title">Account Registration</h1>
    </md-toolbar>
    <md-theme md-name="form">

    <form class="profile-form">
      <p>BassCloud account registration is free and it will allow you to better
      keep track of your favorite content or upload your own projects.</p>
      <p>Please note that BassCloud Service is currently in testing phase,
      in which all content is available for free.
      Later, in order to fulfil main goals of this project and keep it alive,
      only a limited amount of content will be accessible for free.</p>

      <md-input-container :class="{ 'md-input-invalid': errors.username }">
        <label>Username</label>
        <md-input
          required
          name="username"
          v-model="form.username">
        </md-input>
        <span class="md-error" v-for="error in errors.username">{{ error.message }}</span>
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

      <md-input-container :class="{ 'md-input-invalid': errors.email }">
        <label>Email</label>
        <md-input
          name="email"
          type="email"
          required
          v-model="form.email">
        </md-input>
        <span class="md-error" v-for="error in errors.email">{{ error.message }}</span>
      </md-input-container>

      <md-input-container
        md-has-password
        :class="{ 'md-input-invalid': errors.password1 }">
        <label>Password</label>
        <md-input
          name="password1"
          type="password"
          required
          v-model="form.password1">
        </md-input>
        <span class="md-error" v-for="error in errors.password1">{{ error.message }}</span>
      </md-input-container>

      <md-input-container
        md-has-password
        :class="{ 'md-input-invalid': errors.password2 }">
        <label>Confirm Password</label>
        <md-input
          name="password2"
          type="password"
          required
          v-model="form.password2">
        </md-input>
        <span class="md-error" v-for="error in errors.password2">{{ error.message }}</span>
      </md-input-container>

      <md-toolbar class="md-warn main md-transparent">
        <template v-if="inProgress">
          <md-spinner
            :md-size="28"
            md-indeterminate>
          </md-spinner>
          <span md-subhead>Creating Account</span>
        </template>

        <div style="flex:1"></div>
        <md-button
          class="md-raised"
          @click.native="$router.back">
          Cancel
        </md-button>
        <md-button
          class="md-raised md-primary"
          @click.native="register"
          :disabled="inProgress">
          Register
        </md-button>
      </md-toolbar>
    </form>
    </md-theme>
    <md-dialog-alert
      md-title="Account was created"
      md-content="Before you can sign in, you must active your account. Actiavation link was sent to your email address."
      @close="onDialogClose"
      ref="confirm">
    </md-dialog-alert>
  </div>
</template>

<script>

export default {
  name: 'user-profile',
  data () {
    return {
      form: {},
      errors: {},
      inProgress: false
    }
  },

  methods: {
    register () {
      this.errors = {}
      var formData = new FormData(this.$el.querySelector('form'));
      this.$http.post(
        'accounts/register/',
        formData
      ).then(response => {
        this.$refs.confirm.open()
      }, response => {
        this.errors = response.data
      }).finally(resp => {
        this.inProgress = false
      })
      this.inProgress = true
    },
    onDialogClose () {
      this.$router.push({ path: '/' })
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
    .md-toolbar {
      > span {
        margin: 0 6px;
        opacity: 0.75;
      }
    }
  }
</style>