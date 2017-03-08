<template>
  <md-dialog ref="login">
    <md-dialog-title>Login</md-dialog-title>

    <md-dialog-content>
      <form>
        <md-input-container>
          <label>Username</label>
          <md-input
            type="text"
            v-model="username">
          </md-input>
        </md-input-container>
        <md-input-container>
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
</template>

<script>
export default {
  name: 'login-dialog',
  data () {
    return {
      username: '',
      password: ''
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
      console.log(`login: ${this.username} ${this.password}`)
    }
  }
}
</script>