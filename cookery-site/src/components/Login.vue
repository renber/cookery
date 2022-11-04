<template>

  <div id="login">
    <b-container>
      <b-row class="text-center"><b-col>
        <img class="logo">
        <div id="logo">
					<h1 class="text-center">
						Cookery
					</h1>
				</div>
      </b-col></b-row>
    </b-container>
    <b-container class="box" style="padding:20px 10px;background-color:rgba(255, 255, 255, 0.5);">
      <b-row><b-col class="text-center">
        <p class="text-center">Bitte melden Sie sich an</p>
      </b-col></b-row>
      <b-row v-if=error_message><b-col class="text-center">
        <p class="text-red"><b>{{error_message}}</b></p>
      </b-col></b-row>

      <b-row><b-col>
        <b-form @submit.prevent="checkCreds">
          <b-form-row> <b-col>
            <b-input-group>
              <template v-slot:prepend>
                <b-input-group-text><b-icon-person /></b-input-group-text>
              </template>

              <b-form-input v-model="username" type="text" placeholder="Benutzername"></b-form-input>
            </b-input-group>
          </b-col></b-form-row>

          <b-form-row> <b-col>
            <b-input-group>
              <template v-slot:prepend>
                <b-input-group-text><b-icon-lock /> </b-input-group-text>
              </template>

              <b-form-input v-model="password" type="password" placeholder="Passwort"></b-form-input>
            </b-input-group>
          </b-col> </b-form-row>

          <b-form-row> <b-col class="text-center">
            <b-spinner v-if="isBusy" variant="primary" type="grow" />
            <b-button v-else type="submit" variant="primary" size="lg">Anmelden</b-button>
          </b-col> </b-form-row>
        </b-form>
      </b-col></b-row>
    </b-container>
  </div>

</template>

<script>
import UserRepository from 'src/repo/UserRepository'

export default {
  name: 'Login',
  data () {
    return {
      section: 'Login',
      loading: '',
      isBusy: false,
      username: '',
      password: '',
      error_message: ''
    }
  },
  methods: {
    async checkCreds () {
      const { username, password } = this

      this.toggleLoading()
      this.resetResponse()
      this.$store.commit('TOGGLE_LOADING')

      try {
        const { data } = await UserRepository.login(username, password)
        this.toggleLoading()
        if (data.user) {
          console.info('Login succeeded for ' + data.user)
          var user = data.user
          var displayName = data.displayName
          var token = data.token

          this.$store.commit('AUTHENTICATE', { user, token })
          this.$store.commit('SET_DISPLAY_NAME', displayName)

          // check if there is a redirect in the query
          // and go to this page if so
          console.log("Redirect: " + this.$route.query.redirect)
          const target = this.$route.query.redirect
          this.$router.push(target ?? '/')
        }
      } catch (error) {
        console.error(error)
        this.$store.commit('TOGGLE_LOADING')
        // still Unauthorized?
        if (error.response && error.response.status === 401) {
          this.error_message = 'Benutzername und/oder Passwort stimmen nicht oder das Nutzerkonto wurde deaktiviert.'
        } else {
          this.error_message = 'Der Server ist nicht erreichbar. Bitte versuchen Sie es später erneut.'
        }
        this.toggleLoading()
      }
    },
    toggleLoading () {
      this.isBusy = !this.isBusy
      this.loading = this.loading === '' ? 'loading' : ''
    },
    resetResponse () {
      this.error_message = ''
    }
  }
}
</script>

<style scoped>

/* make the login box smaller on large resolutions */
@media (min-width: 1200px) {
    .container{
       max-width: 600px;
    }
}

#login {
  padding-top: 10em;
  min-width: 100vw;
  min-height: 100vh;
  background: url('assets/img/login_bg.jpg');
  background-size: cover;
}

@media (max-width: 767px) {
  #login {
    padding-top: 0px;
  }
}

#logo {
	line-height: 120px;
}

#logo a {
	text-decoration: none;
	color: #fff;
}

#logo h1 {
	font-size: 3.5em;
    color: #fff;
	font-family: Lobster, cursive;
	text-shadow: 0 2px 1px #32251B;
}

.logo {
  width: 15em;
  padding: 0.5em;
}
.input-group {
  padding-bottom: 1em;
}
.input-group-addon {
  display: flex;
  align-items: center;
  margin-top: 1px;
  height: calc(1.5em + .75rem);
  color: gray;
  padding: 0 5px;
}
.input-group-addon i {
  width: 32px;
}
.text-red {
    color: darkred;
}
</style>
