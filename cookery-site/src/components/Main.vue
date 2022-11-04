<template>

<div id="bg">
    <div id="bgsh">
        <b-container fluid id="maincontainer">
            <b-row>
                <b-col >
                    <b-navbar toggleable="lg" type="dark" variant="primary">
                        <b-navbar-brand to="/home" id="logo">
                            <h1> {{ title }} </h1>
                        </b-navbar-brand>
                        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

                        <b-collapse id="nav-collapse" is-nav>
                            <b-navbar-nav class="ml-auto">
                                <b-nav-item  tag="b-nav-item" class="pageLink align-bottom" to="/home">Home</b-nav-item>
                                <b-nav-item  tag="b-nav-item" class="pageLink align-bottom" to="/kochen">Kochen</b-nav-item>
                                <b-nav-item  tag="b-nav-item" class="pageLink align-bottom" to="/backen">Backen</b-nav-item>
                                <b-nav-item  tag="b-nav-item" class="pageLink align-bottom" to="/cocktails">Cocktails</b-nav-item>
                                <b-nav-item  tag="b-nav-item" class="pageLink align-bottom" to="/konfiguration">Konfiguration</b-nav-item>
                            </b-navbar-nav>

                            <!-- separator, which is hidden when menu is collapsed -->
                            <b-nav-text class="d-none d-md-none d-lg-block d-xl-block">|</b-nav-text>

                            <b-navbar-nav >
                                <b-nav-item-dropdown id="user-btn" right>
                                    <template #button-content>
                                          <b-icon-person-circle /> {{ user.displayName }}
                                    </template>
                                    <b-dropdown-item to="/konfiguration/profil">Mein Profil</b-dropdown-item>
                                    <b-dropdown-divider />
                                    <b-dropdown-item variant="danger" @click="logout">Abmelden</b-dropdown-item>
                                </b-nav-item-dropdown>
                            </b-navbar-nav>

                        </b-collapse>
                    </b-navbar>
                </b-col>
            </b-row>
            <router-view :key="$route.path" />
        </b-container>
    </div>
</div>

</template>

<script>
// import NavBar from 'components/layout/NavBar'

export default {
  name: 'App',
  components: {
    // NavBar
  },
  data: () => {
      return {
        title: 'Cookery'
      }
  },
  watch:{
    $route (){
        if (this.$route.path.startsWith('/backen'))
        {
          this.title = 'Bakery'
        } else if (this.$route.path.startsWith('/cocktails'))
        {
          this.title = 'Mixery'
        } else {
          this.title = 'Cookery'
        }
    }
  },
  computed: {
    user () {
      return {
        displayName: this.$store.state.displayName
      }
    }
  },
  methods: {
      logout () {
          this.$store.commit('LOGOUT')
          this.$router.push('/login')
      }
  }
}
</script>

<style scoped>

#maincontainer {
    padding-bottom: 20px;
}

@media only screen and (min-width: 1600px) {
    #maincontainer {
        padding-left: 15%;
        padding-right: 15%;
    }
}

@media only screen and (max-width: 1599px) {
    #maincontainer {
        /* reserve space for the vertical scrollbar */
        padding-right: 20px;
    }
}

@media only screen and (max-width: 991px) {
    #bgsh {
        /* reserve space for the vertical scrollbar */
        padding-top: 0px !important;
    }
}

#app {
  /*font-family: Avenir, Helvetica, Arial, sans-serif;*/
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  /* disable horizontal scrollbar */
  overflow-x: hidden;
}

#bg {
    min-width: 100vw;
    min-height: 100vh;
    background: #ad8667 url('assets/img/bg.jpg');
}

#bgsh {
    padding-top: 60px;
    min-height: 400px;
    background: url('assets/img/shadow.png') top left repeat-x;
}

#header {
    position: relative;
    padding: 40px;
    height: 120px;
}

#logo {
    line-height: 120px;
}

#logo a {
    text-decoration: none;
    color: #fff;
}

#logo h1 {
    font-size: 3em;
    font-family: Lobster, cursive;
    text-shadow: 0 2px 1px #32251B;
}

.navbar .pageLink {
        color: #f4eeea !important;
        text-decoration: none !important;
        text-shadow: 0 1px 1px #32251B !important;
        font-size: 1.2em !important;
    }

.navbar .nav-link.active {
        font-size: 130%;
}

</style>

<style>
#user-btn  .dropdown-item:hover, .dropdown-item:focus {
        background-color: orange;
}

.navbar {
    background-color: transparent !important;
}

.navbar a {
    text-decoration: none !important;
}
</style>