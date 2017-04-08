<template>

  <svg class="level-indicator" viewBox="0 0 100 35">
    <!-- <path d="M0 0 L96 0 L100 8 L96 16 L0 16 L3 8 Z" fill="#ddd" /> -->
    <path d="M0.5 0.5 L95.5 0.5 L99.5 8 L95.5 15.5 L0.5 15.5 Z" stroke="#ddd" fill="#eee" />
    <template v-if="value > 0">
      <path :d="activePath" fill="#616161" />
      <text
        y="12.5"
        :x="1+x/2"
        text-anchor="middle"
        fill="#fff">{{ label.numeric }}
      </text>
      <text v-if="value < 6"
        :x="1+(100+x)/2"
        y="12.5"
        text-anchor="middle"
        fill="#555">5
      </text>
    </template>
    <text v-else x="46" y="12.5" text-anchor="middle" fill="#555">
      0/5
    </text>

    <text y="32" class="title" xtext-anchor="middle">{{ label.title }}
      <!-- &nbsp;{{ label.numeric }} / 5 -->
    </text>
  </svg>

</template>

<script>
  import Constants from '../constants.js'

  export default {
    name: 'level-meter',
    props: {
      value: Number
    },
    computed: {
      x() {
        if (this.value !== undefined) {
          return 100*Constants.Difficulties[this.value].numeric/5 - 4
        }
        return 0
      },
      label() {
        if (this.value !== undefined) {
          return Constants.Difficulties[this.value]
        }
        return {numeric: 0, title: ''}
      },
      activePath() {
        const x = this.x
        // return `M0 0 L${x} 0 L${x+5} 8 L${x} 16 L0 16 L3 8 Z`
        return `M0.5 1 L${x} 1 L${x+4} 8 L${x} 15 L0.5 15 Z`
      }
    }
  }
</script>

<style lang="scss">
  .level-indicator {
    height: 16px;
    max-width: 100px;
    text {
      font-style: normal;
      font-weight: 500;
      font-size: 12px;
      &.title {
        font-weight: normal;
        opacity: 0.35;
        font-size: 13px;
      }
    }
  }
</style>