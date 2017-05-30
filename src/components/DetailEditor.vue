<template>
  <div class="page-container">
  <form class="detail-form">

    <md-input-container>
      <label>Title</label>
      <md-input v-model="form.title">
      </md-input>
    </md-input-container>

    <md-input-container>
      <label>Artist</label>
      <md-input v-model="form.artist">
      </md-input>
    </md-input-container>

    <md-input-container
      :class="{
        'md-has-value': form.description,
        'md-input-focused': editorFocused
      }">
      <label>Description</label>
      <input type="hidden"></input>
      <div
        @focus="editorFocused=true"
        @blur="blur"
        class="editor"
        contenteditable="true"
        v-html="compiledMarkdown">
      </div>
    </md-input-container>

<!--     <md-input-container>
      <label>Description</label>
      <md-textarea v-model="form.description">
      </md-textarea>
    </md-input-container> -->

    <div class="field-group">
      <md-input-container>
        <label>Category</label>
        <md-select v-model="form.category">

          <md-option
            v-for="category in Categories"
            :value="category">{{ category }}
          </md-option>

        </md-select>
      </md-input-container>

      <md-input-container>
        <label>Difficulty</label>
        <md-select v-model="form.level">
          <md-option
            v-for="(label, value) in Difficulties"
            :value="parseInt(value)">{{ label.title }}
          </md-option>
        </md-select>
      </md-input-container>
    </div>

    <div class="field-group">
      <md-chips
        v-chips-label="'Musical Genres'"
        v-model="form.genres"
        class="with-label"
        md-input-placeholder="Add musical genre"
        @change="standardizeGenres">
        <template scope="chip">{{ chip.value }}</template>
      </md-chips>

      <md-input-container>
        <label>Playing Styles</label>
        <md-select
          multiple
          name="playing_styles"
          v-model="form.playing_styles">
          <md-option
            v-for="style in PlayingStyles"
            :value="style">{{ style }}
          </md-option>
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

    <md-input-container>
      <label>Video Link</label>
      <md-input v-model="form.video_link">
      </md-input>
    </md-input-container>

    <md-toolbar class="md-warn main md-transparent">
      <div style="flex:1"></div>
      <md-button
        class="md-raised"
        @click.native="$router.back">
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
import Constants from '../constants.js'
import marked from 'marked'
import '../lib/pen/pen.css'
import pen from '../lib/pen/pen'

export default {
  name: 'detail-editor',
  data () {
    return {
      form: {
        playing_styles: [],
        description: ''
      },
      editorFocused: false
    }
  },
  computed: {
    project() {
      return this.$parent.project
    },
    compiledMarkdown: function () {
      /*
      if (this.project.description) {
        return marked(this.project.description, { sanitize: true })
          // .replace(/<strong>/g, '<b>').replace(/<\/strong>/g, '</b>')
      }*/
      if (this.form.description) {
        return marked(this.form.description, { sanitize: false })
      }
      return ''
    }
  },
  created () {
    this.Difficulties = Constants.Difficulties
    this.Categories = Constants.Categories
    this.PlayingStyles = Constants.PlayingStyles
    if (this.project.id) {
      this.initializeForm()
    }
  },
  mounted () {
    this.editor = new Pen({
      class: 'description',
      editor: document.querySelector('.editor'),
      list: ['h1', 'h2', 'bold', 'italic', 'underline', 'insertorderedlist',
            'insertunorderedlist', 'superscript', 'subscript', 'createlink'],
      toolbarParent: document.querySelector('.editor').parentElement
    });
  },
  watch: {
    project (newVal, oldVal) {
      console.log('project changed')
      this.initializeForm()
    }
  },
  methods: {
    initializeForm() {
      let form = {}
      const fields = [
        'id', 'title', 'artist', 'description', 'category', 'video_link',
        'level', 'genres', 'playing_styles', 'tags', 'tracks'
      ]
      fields.forEach(key => {
        form[key] = this.project[key]
      })
      form.video_link = this.$options.filters.videolink(form.video_link)
      this.form = form
    },
    standardizeGenres() {
      this.form.genres = Constants.MusicalStyles.from(this.form.genres)
    },
    save() {
      // var formData = new FormData(this.$el.querySelector('form'));
      this.$client.updatePorject(this.form)
        .then(response => {
          for (const key in this.form) {
            this.project[key] = this.form[key]
          }
          this.$router.back()
        })
    },
    blur() {
      this.editorFocused = false
      this.form.description = this.editor.toMd()
    }
  }
}
</script>
<style lang="scss">
  .md-input-container.md-has-value .pen-menu input.pen-input {
    color: #fff;
    font-size: 14px;
    &::-webkit-input-placeholder {
      color: #bbb;
      font-size: 14px;
    }
  }
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
    /* temporary workaround for auto-height issue until next Vue-Material version */
    textarea.md-input {
      min-height: 130px;
      max-height: 500px;
    }
    .editor {
      padding-top: 6px;
      outline: none;
      width: 100%;
      > p:first-child {
        margin: 0;
      }
    }
  }
</style>