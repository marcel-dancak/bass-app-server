<template>
  <div>
  <md-toolbar class="md-warn main">
    <h1 class="md-title">Profile</h1>
  </md-toolbar>
  <form>
    <md-input-container>
      <label>Username</label>
      <md-input v-model="form.username" disabled></md-input>
    </md-input-container>
    <md-input-container>
      <label>Profile Photo</label>
      <md-file v-model="form.avatar" accept="image/*" name="avatar"></md-file>
    </md-input-container>
    <md-input-container>
      <label>First Name</label>
      <md-input v-model="form.first_name" name="first_name"></md-input>
    </md-input-container>
    <md-input-container>
      <label>Last Name</label>
      <md-input v-model="form.last_name" name="last_name"></md-input>
    </md-input-container>
    <md-input-container>
      <label>E-mail</label>
      <md-input v-model="form.email" required type="email" name="email"></md-input>
    </md-input-container>


  <md-toolbar class="md-warn main md-transparent">
    <div style="flex:1"></div>
    <md-button
      class="md-raised"
      @click.native="back">
      Cancel
    </md-button>
    <md-button
      class="md-raised"
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
  components: {
  },
  props: {
  },
  data () {
    return {
      form: {},
    }
  },
  created () {
    ['id', 'username', 'first_name', 'last_name', 'email'].forEach(key => {
      this.form[key] = this.$root.$data.user[key]
    })
  },
  methods: {
    back() {
      this.$router.go(-1)
    },
    save() {
      console.log(this.$el)
      var formData = new FormData(this.$el.querySelector('form'));
      console.log(formData)
      // formData.append('avatar', );
      this.$http.post(
        'profile/',
        formData
      ).then(response => {
        this.$root.updateUser(response.data)
        // this.$forceUpdate()
        this.$router.back()
      })
    }
  }
}
</script>
<style lang="scss" scoped>
  form {
    padding: 16px;
    max-width: 600px;
  }
</style>