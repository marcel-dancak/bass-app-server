<template>
  <md-theme md-name="form">
    <md-dialog
      ref="feedback"
      class="feedback-dialog"
      @open="initialize">
      <md-dialog-title>
        Leave Feedback
        <md-spinner
          :md-size="28"
          md-indeterminate
          v-show="inProgress">
        </md-spinner>
      </md-dialog-title>

      <md-dialog-content>
        <form
          novalidate
          @submit.stop.prevent="submit">
          <br />
          <md-input-container :class="{ 'md-input-invalid': errors.email }">
            <label>Your Email</label>
            <md-input
              name="email"
              type="email"
              v-model="form.email">
            </md-input>
            <span
              v-for="error in errors.email"
              class="md-error">{{ error.message }}
            </span>
          </md-input-container>

          <md-input-container :class="{ 'md-input-invalid': errors.message }">
            <label>Message</label>
            <md-textarea
              name="message"
              type="text"
              v-model="form.message">
            </md-textarea>
            <span
              v-for="error in errors.message"
              class="md-error">{{ error.message }}
            </span>
          </md-input-container>
        </form>
      </md-dialog-content>

      <md-dialog-actions>
        <md-button
          class="md-raised"
          @click.native="close">
          Cancel
        </md-button>
        <md-button
          :disabled="inProgress"
          class="md-raised md-primary"
          @click.native="send">
          Send
        </md-button>
      </md-dialog-actions>
    </md-dialog>
  </md-theme>
</template>

<script>
export default {
  name: 'feedback-dialog',
  data () {
    return {
      form: {
        email: '',
        message: ''
      },
      errors: {},
      inProgress: false
    }
  },
  methods: {
    open() {
      this.$refs.feedback.open()
    },
    close() {
      this.$refs.feedback.close()
    },
    initialize() {
      if (this.$store.state.user) {
        this.form.email = this.$store.state.user.email
      }
      this.form.message = ''
      this.errors = {}
      this.inProgress = false
    },
    send() {
      this.errors = {}
      var formData = new FormData(this.$el.querySelector('form'))
      if (!formData.get('message')) {
        this.errors = {message: [{message: 'Message field is required'}]}
        return
      }
      this.inProgress = true
      this.$http.post(
        'feedback/',
        formData
      ).then(response => {
        this.inProgress = false
        this.close()
        this.$emit('sent')
      }, response => {
        this.inProgress = false
        this.errors = response.data
        this.$emit('error')
      })
    }
  }
}
</script>

<style lang="scss">
  .feedback-dialog {
    .md-dialog {
      min-height: 324px;
      min-width: 290px;
      max-width: 290px;
      @media (min-width: 401px) {
        width: 800px;
        max-width: 80%;
      }
      @media (min-width: 1024px) {
        max-width: 60%;
      }
    }
    .md-spinner {
      position: absolute;
      right: 33px;
    }
    textarea {
      min-height: 76px;
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