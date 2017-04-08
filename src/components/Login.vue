<template>
  <md-theme md-name="form">
    <md-dialog
      ref="login"
      class="login-dialog"
      @open="initialize">
      <md-dialog-title>
        {{ forgottenPassword? 'Reset Password' : 'Login' }}
        <md-spinner
          :md-size="28"
          md-indeterminate
          v-show="inProgress">
        </md-spinner>
      </md-dialog-title>

      <md-dialog-content>
        <form
          @keyup.enter="login"
          novalidate @submit.stop.prevent="submit">
          <template v-if="!forgottenPassword">
            <md-input-container :class="{'md-input-invalid': loginErrors.username}">
              <label>Username</label>
              <md-input
                name="username"
                type="text">
              </md-input>
              <span
                v-for="error in loginErrors.username"
                class="md-error">{{ error.message }}
              </span>
            </md-input-container>
            <md-input-container
              md-has-password
              :class="{'md-input-invalid': loginErrors.password}">
              <label>Password</label>
              <md-input
                name="password"
                type="password">
              </md-input>
              <span
                v-for="error in loginErrors.password"
                class="md-error">{{ error.message }}
              </span>
            </md-input-container>
            <md-input-container
              v-if="loginErrors.__all__"
              class="errors-all md-input-invalid">
              <md-input type="hidden"></md-input>
              <span
                v-for="error in loginErrors.__all__"
                class="md-error">{{ error.message }}
              </span>
            </md-input-container>

            <a @click="forgottenPassword=true">Forgotten password</a>
          </template>
          <template v-else>
            <br />
            <p v-if="passwordResetSent" class="success">
              Verification email was sent to your email address
            </p>
            <p v-else class="info">
              Enter email address associated with your account
            </p>
            <br />
            <md-input-container :class="{ 'md-input-invalid': resetErrors.email }">
              <label>Email</label>
              <md-input
                name="email"
                type="email">
              </md-input>
              <span
                v-for="error in resetErrors.email"
                class="md-error">{{ error.message }}
              </span>
            </md-input-container>
            <a @click="forgottenPassword=false">Back to regular login</a>
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
      loginErrors: {},
      resetErrors: {},
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
      this.loginErrors = {}
      this.resetErrors = {}
      this.inProgress = false
      this.forgottenPassword = false
      this.passwordResetSent = false
    },
    login() {
      this.inProgress = true
      this.loginErrors = {}
      var formData = new FormData(this.$el.querySelector('form'))
      this.$http.post(
        'login/',
        formData
      ).then(response => {
        this.inProgress = false
        this.close()
        this.$store.commit('updateProfile', response.data)
        this.$emit('login', response.data)
      }, response => {
        this.inProgress = false
        this.loginErrors = response.data
        // TODO: custom error when empty response?
      })
    },
    resetPassword () {
      this.inProgress = true
      this.resetErrors = {}
      var formData = new FormData(this.$el.querySelector('form'))
      this.$http.post(
        'accounts/password_reset/',
        formData
      ).then(response => {
        this.passwordResetSent = true
      }, response => {
        this.resetErrors = response.data
      }).finally(response => {
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
      max-width: 380px;
      min-height: 324px;
      @media (max-width: 400px) {
        min-width: 290px;
        max-width: 290px;
      }
    }
    .md-spinner {
      position: absolute;
      right: 33px;
    }
    .info {
      opacity: 0.85;
    }
    .success {
      color: #1e88e5;
    }
    .errors-all {
      padding-top: 0;
      &:after {
        display: none;
      }
      .md-error {
        bottom: auto;
      }
    }
    .md-dialog-actions {
      padding: 0 16px;
      margin-bottom: 8px;
      .md-button {
        padding: 0 16px;
      }
    }
  }
</style>