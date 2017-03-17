import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {
        likes: [],
        favourites: [],
        subscribers: []
    }
  },
  mutations: {
    updateProfile (state, profile) {
      state.user = profile
    }
  }
})