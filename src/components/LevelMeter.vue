<template>

<!--   <svg class="level-meter" viewBox="0 0 42 16">
    <rect x="0.5" y="0.5" width="41" height="15" stroke-width="1" stroke="#212121" fill="#f5f5f5" />
    <rect x="1" y="1" :width="width" height="14" fill="#616161" />
    <rect x="9" y="1" width="1" height="14" fill="#212121" />
    <rect x="17" y="0" width="1" height="16" fill="#212121" />
    <rect x="24" y="0" width="1" height="16" fill="#212121" />
    <rect x="32" y="0" width="1" height="16" fill="#212121" />
  </svg> -->

<!--   <svg class="level-meter" viewBox="0 0 42 16">
    <rect x="0.5" y="0.5" width="41" height="15" stroke-width="1" stroke="#212121" fill="#f5f5f5" />
    <rect x="1" y="1" :width="width" height="14" fill="#424242" />
    <rect x="9" y="1" width="1" height="14" fill="#424242" opacity="0.4" />
    <rect x="17" y="0" width="1" height="16" fill="#424242" opacity="0.4" />
    <rect x="25" y="0" width="1" height="16" fill="#424242" opacity="0.4" />
    <rect x="33" y="0" width="1" height="16" fill="#424242" opacity="0.4" />
  </svg> -->

<!-- LEVEL 3 -->
<!--   <svg class="level-meter" viewBox="0 0 42 16">
    <rect x="0.5" y="0.5" width="41" height="15" stroke-width="1" stroke="#212121" fill="#f5f5f5" />
    <rect x="1" y="1" :width="level3" height="14" fill="#424242" />
    <rect x="12" y="1" width="1" height="14" fill="#424242" opacity="0.3" />
    <rect x="27" y="1" width="1" height="14" fill="#424242" opacity="0.3" />
  </svg> -->

<!-- LEVEL 5 -->
<!--   <svg class="level-meter" viewBox="0 0 42 16">
    <rect x="0.5" y="0.5" width="41" height="15" stroke-width="1" stroke="#212121" fill="#f5f5f5" />
    <rect x="1" y="1" :width="level5" height="14" fill="#424242" />
  </svg> -->

<!-- LEVEL 7 -->
  <svg class="level-meter7" viewBox="0 0 37 16">
    <rect x="0.5" y="0.5" width="36" height="15" stroke-width="1" stroke="#424242" fill="#f5f5f5" />
    <rect x="1" y="1" :width="level7" height="14" fill="#616161" />
    <!-- <line x1="6.5" x2="6.5" y1="1" y2="16" stroke="#424242" opacity="0.4" /> -->
    <rect v-for="i in 5" :x="i*6" y="1" width="1" height="14" fill="#9E9E9E" opacity="0.5" />

<!--     <rect x="6" y="1" width="1" height="14" fill="#9E9E9E" opacity="0.8" />
    <rect x="12" y="0" width="1" height="16" fill="#BDBDBD" opacity="0.8" />
    <rect x="18" y="0" width="1" height="16" fill="#424242" opacity="0.4" />
    <rect x="24" y="0" width="1" height="16" fill="#424242" opacity="0.4" />
    <rect x="30" y="0" width="1" height="16" fill="#424242" opacity="0.4" /> -->
  </svg>

<!--   <svg class="level-meter" viewBox="0 0 42 16">
    <rect x="0.5" y="0.5" width="41" height="15" stroke-width="1" stroke="#212121" fill="#f5f5f5" />
    <rect x="1" y="1" :width="width" height="14" fill="#424242" />
    <rect v-for="i in 4" :x="8*i+1"
      y="1" width="1" height="14" fill="#424242" opacity="0.3" />
  </svg> -->

<!--   <svg class="analog-meter" viewBox="0 0 42 24">
    <path d="M0.5 23.5 A 21 23.5 0 0 1 41 23.5 Z" stroke="#424242" fill="#f5f5f5"/>
    <path :d="test" fill="#424242"/>
  </svg> -->

</template>

<script>

function deg2rad(value) {
  return value * Math.PI / 180;
}

const LEVEL_3 = {
  1: 1,
  2: 1,
  3: 1,
  4: 2,
  5: 2,
  6: 3,
  7: 3
}
// const LEVEL_5 = {
//   1: 1,
//   2: 2,
//   3: 2.5,
//   4: 3,
//   5: 3.5,
//   6: 4,
//   7: 5
// }
const LEVEL_5 = {
  1: 0.75,
  2: 1.25,
  3: 2,
  4: 2.75,
  5: 3.5,
  6: 4.35,
  7: 5
}

export default {
  name: 'level-meter',
  props: {
    value: Number
  },
  computed: {
    width() {
      const normalized = {
        1: 1,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 5
      }[this.value]
      return Math.round(41*(normalized/5))
    },
    level3() {
      return Math.round(41*(LEVEL_3[this.value]/3))
    },
    level5() {
      return Math.round(41*(LEVEL_5[this.value]/5))
    },
    level7() {
      return Math.round(36*(this.value/6))
    },
    test() {
      const coords = this.convert_to_svg(21, 24, 21, 18, -180, (180/6)*this.value, 0)
      const arc = coords.slice(2).join(' ')
      return `M${coords[0]} ${coords[1]} A ${arc} L21, 23.5 Z`
    }
  },
  methods: {
    convert_to_svg(cx, cy, rx, ry, theta1, delta, phi) {
      let theta2 = delta + theta1
      theta1 = deg2rad(theta1)
      theta2 = deg2rad(theta2)
      const phi_r = deg2rad(phi)

      //   Figure out the coordinates of the beginning and
      //   ending points

      const x0 = cx + Math.cos(phi_r) * rx * Math.cos(theta1) +
          Math.sin(-phi_r) * ry * Math.sin(theta1)
      const y0 = cy + Math.sin(phi_r) * rx * Math.cos(theta1) +
          Math.cos(phi_r) * ry * Math.sin(theta1)

      const x1 = cx + Math.cos(phi_r) * rx * Math.cos(theta2) +
          Math.sin(-phi_r) * ry * Math.sin(theta2)
      const y1 = cy + Math.sin(phi_r) * rx * Math.cos(theta2) +
          Math.cos(phi_r) * ry * Math.sin(theta2)

      const large_arc = (delta > 180) ? 1 : 0
      const sweep = (delta > 0) ? 1 : 0
      
      return [x0, y0, rx, ry, phi, large_arc, sweep, x1, y1]
    }
  }
}
</script>

<style lang="scss">
  .level-meter {
    width: 42px;
    height: 16px;
    max-width: 42px;
    opacity: 0.75;
    border-radius: 2px;
  }
  .level-meter7 {
    width: 37px;
    height: 16px;
    max-width: 37px;
    opacity: 0.9;
  }
  .analog-meter {
    width: 42px;
    height: 24px;
    max-width: 42px;
  }
  .level {
    width: 24px;
    height: 24px;
    background-color: #444;
    color: #fff;
    text-align: center;
    line-height: 24px;
    border-radius: 12px;
  }
</style>