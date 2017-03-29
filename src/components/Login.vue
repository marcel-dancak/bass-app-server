<template>
  <md-theme md-name="form">
    <md-dialog
      ref="login"
      class="login-dialog"
      @open="initialize">
      <md-dialog-title>Login</md-dialog-title>

      <md-dialog-content>
        <div class="progress-box">
          <md-progress md-indeterminate v-show="inProgress"></md-progress>
        </div>
        <form
          @keyup.enter="login"
          novalidate @submit.stop.prevent="submit">
          <template v-if="!forgottenPassword">
            <md-input-container :class="{'md-input-invalid': error}">
              <label>Username</label>
              <md-input
                name="username"
                type="text">
              </md-input>
            </md-input-container>
            <md-input-container
              md-has-password
              :class="{'md-input-invalid': error}">
              <label>Password</label>
              <md-input
                name="password"
                type="password">
              </md-input>
            </md-input-container>
            <a @click="forgottenPassword=true">Forgotten password</a>
          </template>
          <template v-else>
            <md-input-container>
              <label>E-mail</label>
              <md-input
                name="email"
                type="email">
              </md-input>
            </md-input-container>
            <p v-if="passwordResetSent">
              Request to reset your password was received, please check your e-mail account for more details.
            </p>
            <a v-else
              @click="forgottenPassword=false">Back to regular login
            </a>
          </template>
        </form>
      </md-dialog-content>

      <md-dialog-actions>
        <md-button
          class="md-raised"
          @click.native="close">
          Cancel
        </md-button>
        <md-button
          v-if="forgottenPassword"
          :disabled="inProgress || passwordResetSent"
          class="md-raised md-primary"
          @click.native="resetPassword">
          Reset Password
        </md-button>
        <md-button
          v-else
          :disabled="inProgress"
          class="md-raised md-primary"
          @click.native="login">
          Login
        </md-button>
      </md-dialog-actions>
    </md-dialog>
  </md-theme>
</template>

<script>
export default {
  name: 'login-dialog',
  data () {
    return {
      error: false,
      inProgress: false,
      forgottenPassword: false,
      passwordResetSent: false
    }
  },
  methods: {
    open() {
      this.$refs.login.open()
    },
    close() {
      this.$refs.login.close()
    },
    initialize() {
      this.error = false
      this.inProgress = false
      this.forgottenPassword = false
      this.passwordResetSent = false
    },
    login() {
      this.inProgress = true
      var formData = new FormData(this.$el.querySelector('form'))
      this.$http.post(
        'login/',
        formData
      ).then(response => {
        this.error = false
        this.inProgress = false
        this.close()
        this.$emit('login', response.data)
      }, response => {
        this.inProgress = false
        if (response.status === 401) {
          this.error = true
        }
      })
    },
    resetPassword () {
      this.inProgress = true
      var formData = new FormData(this.$el.querySelector('form'))
      this.$http.post(
        'accounts/password_reset/',
        formData
      ).then(response => {
        this.inProgress = false
        this.passwordResetSent = true
      }, response => {
        this.inProgress = false
      })
    }
  }
}
</script>

<style lang="scss">
  .login-dialog {
    .md-dialog {
      min-width: 320px;
    }
    .md-dialog-actions {
      padding: 0 16px;
      margin-bottom: 8px;
      .md-button {
        padding: 0 16px;
      }
    }
    .progress-box {
      height: 10px;
    }
  }
</style>