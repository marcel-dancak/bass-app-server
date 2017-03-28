<template>
  <md-theme md-name="form">
    <md-dialog
      ref="login"
      @open="error=false">
      <md-dialog-title>Login</md-dialog-title>

      <md-dialog-content>
        <form
          @keyup.enter="login"
          novalidate @submit.stop.prevent="submit">
          <md-input-container :class="{'md-input-invalid': error}">
            <label>Username</label>
            <md-input
              type="text"
              v-model="username">
            </md-input>
          </md-input-container>
          <md-input-container
            md-has-password
            :class="{'md-input-invalid': error}">
            <label>Password</label>
            <md-input
              type="password"
              v-model="password">
            </md-input>
          </md-input-container>
        </form>
      </md-dialog-content>

      <md-dialog-actions>
        <md-button
          class="md-primary"
          @click.native="close">
          Cancel
        </md-button>
        <md-button
          class="md-primary"
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
      username: '',
      password: '',
      error: false
    }
  },
  methods: {
    open() {
      this.$refs.login.open()
    },
    close() {
      this.$refs.login.close()
    },
    login() {
      this.$http.post(
        'login/',
        {
          username: this.username,
          password: this.password
        }
      ).then(response => {
        this.error = false
        this.close()
        this.$emit('login', response.data)
      }, response => {
        if (response.status === 401) {
          this.error = true
        }
      })
    }
  }
}

</script>
