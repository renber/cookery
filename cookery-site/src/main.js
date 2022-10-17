// third-party css files
import '@/assets/css/bootstrap-custom.scss'

// our css files
import '@/assets/css/main.css'
import '@/assets/css/fonts.css'

import Vue from 'vue'
import VueRouter from 'vue-router'

import { sync } from 'vuex-router-sync'
import routes from './routes'
import { store } from 'src/store'

import App from './components/App.vue'

Vue.use(VueRouter)

// bootstrap-vue
import {
  LayoutPlugin, TablePlugin, PaginationPlugin,
  SpinnerPlugin, ModalPlugin, FormGroupPlugin, FormInputPlugin,
  InputGroupPlugin, ButtonPlugin, ButtonToolbarPlugin,
  ButtonGroupPlugin, DropdownPlugin, FormPlugin, CardPlugin,
  FormRadioPlugin, IconsPlugin, FormTagsPlugin, FormTextareaPlugin,
  BadgePlugin, TooltipPlugin, NavbarPlugin, FormSpinbuttonPlugin 
} from 'bootstrap-vue'

Vue.config.productionTip = false

// setup vue-bootstrap components
Vue.use(LayoutPlugin)
Vue.use(TablePlugin)
Vue.use(NavbarPlugin)
Vue.use(PaginationPlugin)
Vue.use(SpinnerPlugin)
Vue.use(ModalPlugin)
Vue.use(ButtonPlugin)
Vue.use(InputGroupPlugin)
Vue.use(FormPlugin)
Vue.use(FormGroupPlugin)
Vue.use(FormInputPlugin)
Vue.use(ButtonToolbarPlugin)
Vue.use(ButtonGroupPlugin)
Vue.use(DropdownPlugin)
Vue.use(CardPlugin)
Vue.use(FormRadioPlugin)
Vue.use(IconsPlugin)
Vue.use(FormTagsPlugin)
Vue.use(FormTextareaPlugin)
Vue.use(BadgePlugin)
Vue.use(TooltipPlugin)
Vue.use(FormSpinbuttonPlugin)

// Routing logic
var router = new VueRouter({
  base: process.env.NODE_ENV === 'production' ? '/cookery/' : '',
  routes: routes,
  mode: 'history',
  // linkExactActiveClass: 'active',
  linkActiveClass: 'active',
  scrollBehavior: function (to, from, savedPosition) {
    return savedPosition || { x: 0, y: 0 }
  }
})

// Some middleware to help us ensure that the user is authenticated.
router.beforeEach((to, from, next) => {
  if (
    to.matched.some(record => record.meta.requiresAuth) &&
    (!router.app.$store.state.token || router.app.$store.state.token === 'null')
  ) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    window.console.log('Not authenticated')
    next({
      name: 'login',
      query: { redirect: to.path }
    })
  } else {
    if (to.path === '/' || to.path === '') {
      next({ name: 'home' })
    } else {
      next()
    }
  }
})

sync(store, router)

// Check local storage to handle refreshes
if (window.localStorage) {
  var localUserString = window.localStorage.getItem('user') || 'null'
  var localUser = JSON.parse(localUserString)
  var displayName = JSON.parse(window.localStorage.getItem('displayName'))

  if (localUser && displayName && store.state.user !== localUser) {
    var user = localUser
    var token = window.localStorage.getItem('token')
    store.commit('AUTHENTICATE', { user, token })

    store.commit('SET_DISPLAY_NAME', displayName)
  }
}

new Vue({
  router: router,
  store: store,
  render: h => h(App),
}).$mount('#app')
