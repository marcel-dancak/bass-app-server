<template>
  <div class="page-container">
  <form class="detail-form">

    <md-input-container>
      <label>Title</label>
      <md-input
        name="title"
        v-model="form.title">
      </md-input>
    </md-input-container>

    <md-input-container>
      <label>Artist</label>
      <md-input
        name="artist"
        v-model="form.artist">
      </md-input>
    </md-input-container>

    <div class="field-group">
      <md-input-container>
        <label>Category</label>
        <md-select
          name="category"
          v-model="form.category">
          <md-option value="cover">Cover</md-option>
          <md-option value="lesson">Lesson</md-option>
          <md-option value="arrangement">Arrangement</md-option>
          <md-option value="composition">Original Composition</md-option>
          <md-option value="backing_track">Backing Track</md-option>
        </md-select>
      </md-input-container>
      <md-input-container>
        <label>Level</label>
        <md-select
          name="level"
          v-model="form.level">
          <md-option :value="1">Easy</md-option>
          <md-option :value="2">Medium</md-option>
          <md-option :value="3">Hard</md-option>
          <md-option :value="4">Extreme</md-option>
        </md-select>
      </md-input-container>
    </div>

    <md-input-container>
      <label>Description</label>
      <md-textarea
        name="description"
        v-model="form.description">
      </md-textarea>
    </md-input-container>

    <md-input-container>
      <label>Video Link</label>
      <md-input
        name="video_link"
        v-model="form.video_link">
      </md-input>
    </md-input-container>

    <div class="field-group">
<!--     <md-chips
      v-chips-label="'Playing Styles'"
      v-model="form.playing_styles"
      class="with-label"
      md-input-placeholder="Add playing style">
      <template scope="chip">{{ chip.value }}</template>
    </md-chips>
    <input name="playing_styles" type="hidden" :value="formatArrayValue(form.playing_styles)"> -->


      <md-chips
        v-chips-label="'Musical Genres'"
        v-model="form.genres"
        class="with-label capitalize"
        md-input-placeholder="Add musical genre">
        <template scope="chip">{{ chip.value }}</template>
      </md-chips>
      <input name="genres" type="hidden" :value="formatArrayValue(form.genres)">

      <md-input-container>
        <label>Playing Styles</label>
        <md-select
          multiple
          name="playing_styles"
          v-model="form.playing_styles">
          <md-option value="finger">Finger</md-option>
          <md-option value="slap">Slap</md-option>
          <md-option value="tap">Tap</md-option>
          <md-option value="pick">Pick</md-option>
        </md-select>
      </md-input-container>
    </div>

    <md-chips
      v-chips-label="'Tags'"
      v-model="form.tags"
      class="with-label"
      md-input-placeholder="Add tag">
      <template scope="chip">{{ chip.value }}</template>
    </md-chips>
    <input name="playing_styles" type="hidden" :value="formatArrayValue(form.tags)">

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
  name: 'detail-editor',
  data () {
    return {
      form: {
        playing_styles: []
      },
    }
  },
  computed: {
    project() {
      return this.$parent.project
    }
  },
  created () {
    if (this.project.id) {
      this.initializeForm()
    }
  },
  watch: {
    project (newVal, oldVal) {
      console.log('project changed')
      this.initializeForm()
    }
  },
  methods: {
    back() {
      this.$router.go(-1)
    },
    initializeForm() {
      let form = {}
      const fields = [
        'id', 'title', 'artist', 'description', 'category', 'video_link',
        'level', 'genres', 'playing_styles', 'tags', 'tracks'
      ]
      fields.forEach(key => {
          form[key] = this.project[key]
        })
      this.form = form
    },
    formatArrayValue(array) {
      return array? array.join(',') : ''
    },
    save() {
      var formData = new FormData(this.$el.querySelector('form'));
      this.$http.post(
        'project/',
        // formData
        this.form
      ).then(response => {
        for (const key in this.form) {
          // this.$parent.project
          this.project[key] = this.form[key]
        }
        this.$router.back()
      })
    }
  }
}
</script>
<style lang="scss">

  .md-menu-content {
    min-width: 200px;
  }
  .detail-form {
    padding: 16px;
    max-width: 800px;
    .md-chips {
      .md-chip + .md-input::-webkit-input-placeholder {
        visibility: hidden;
      }
    }
    .field-group {
      display: flex;
      > *:not(:last-child) {
        margin-right: 24px;
      }
      > * {
        flex: 50%;
      }
      > .md-input-container {
        align-self: flex-end;
        xpadding-top: 24px;
      }
    }
  }
</style>