import axios from 'axios'

export default {
  TOGGLE_LOADING (state) {
    state.callingAPI = !state.callingAPI
  },
  TOGGLE_SEARCHING (state) {
    state.searching = (state.searching === '') ? 'loading' : ''
  },
  SET_DISPLAY_NAME (state, displayName) {
    state.displayName = displayName
    if (window.localStorage) {
      window.localStorage.setItem('displayName', JSON.stringify(displayName))
    }
  },
  AUTHENTICATE (state, { user, token }) {
    state.user = user
    state.token = token

    // write current user-data to local storage, so that we
    // can read it after a restart
    if (window.localStorage) {
      window.localStorage.setItem('user', JSON.stringify(user))
      window.localStorage.setItem('token', token)
    }
  },
  LOGOUT (state) {
    // delete session information
    state.user = null
    state.token = null
    axios.defaults.headers.common.Authorization = null

    if (window.localStorage) {
      window.localStorage.removeItem('user')
      window.localStorage.removeItem('displayName')
      window.localStorage.removeItem('token')
    }
  }
}
