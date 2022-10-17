<!-- Startpage of the configuration page -->

<template>
     <div>
        Auf dieser Seite können Sie die zu ihrem Benutzerkonto hinterlegten
        Informationen anpassen.    
        <br>    
        <br>

    <b-form @submit.prevent="submit" autocomplete="off">
         <b-card bg-variant="light">
            <b-form-group
            label-cols-lg="3"
            label="Allgemeine Informationen"
            label-size="lg"
            label-class="font-weight-bold pt-0"
            class="mb-0">

            <b-form-group            
            label="Nutzername:"
            label-for="username-input"
            description="">
            <b-form-input
              id="username-input"
              type="text"
              value=""
            ></b-form-input>
          </b-form-group>

          <b-form-group            
            label="Anzeigename:"
            label-for="user-displayname-input"
            description="">
            <b-form-input
              id="user-displayname-input"
              type="text"
              value=""
            ></b-form-input>
          </b-form-group>          

            </b-form-group>

            <!--
          <div v-if="modals.addIngredient.errorMessage" class="error-message">
            {{ modals.addIngredient.errorMessage }}
          </div>-->

          <b-button type="submit" variant="success">Änderungen übernehmen</b-button>
         </b-card>            
        </b-form>       

        <br>

        <b-form @submit.prevent="updatePassword" autocomplete="off">
          <b-card bg-variant="light">
            <b-form-group
            label-cols-lg="3"
            label="Passwort ändern"
            label-size="lg"
            label-class="font-weight-bold pt-0"
            class="mb-0">

            <b-form-group
                label="Bisheriges Passwort:"
                label-for="current-password-input"
                label-cols-sm="3"
                label-align-sm="right">
                <b-form-input id="current-password-input" type="password" v-model="changePwd.oldPwd"></b-form-input>
            </b-form-group>    

            <b-form-group
                label="Neues Passwort:"
                label-for="new-password-input"
                label-cols-sm="3"
                label-align-sm="right">
                <b-form-input id="new-password-input" type="password" :state="newPasswordState" v-model="changePwd.newPwd"></b-form-input>
                <b-form-invalid-feedback id="input-live-feedback">
                  Das Passwort muss mindestens 8 Zeichen lang sein
                </b-form-invalid-feedback>
            </b-form-group>    
            <b-form-group
                label="Neues Passwort (Wiederholung):"                
                label-for="new-password-repetition-input"
                label-cols-sm="3"
                label-align-sm="right">                 
                <b-form-input id="new-password-repetition-input" type="password" :state="newPasswordRepState" v-model="changePwd.newPwdRep"></b-form-input>
                <b-form-invalid-feedback id="input-live-feedback">
                  Die Eingaben weichen voneinander ab
                </b-form-invalid-feedback>
            </b-form-group>    

            </b-form-group>

          <b-button type="submit" variant="success">Passwort ändern</b-button>          
          
          <div style="height:10px" />
          <b-alert :show="changePwd.errorText !== ''" variant="danger" dismissible fade>
            {{ changePwd.errorText }}
          </b-alert>

          <b-alert :show="changePwd.successText !== ''" variant="success" dismissible fade>
            {{ changePwd.successText }}
        </b-alert>
        </b-card>        
        </b-form>        
    </div>
</template>

<script>
import UserRepository from "src/repo/UserRepository"

import { BAlert } from 'bootstrap-vue'

export default {
    name: 'config-profile',
    components: {
      BAlert
    },
    data: () => {
      return {
          changePwd: {
            errorText: '',
            successText: '',
            oldPwd: '',
            newPwd: '',
            newPwdRep: ''            
          }
        }
    },
    computed: {
      newPasswordState() {
        return this.changePwd.newPwd.length >= 8
      },
      newPasswordRepState() {
        if (this.changePwd.newPwd === '') {
          return null
        }
        return this.changePwd.newPwd === this.changePwd.newPwdRep
      }
    },
    methods: {
      async updatePassword () {
        try {
          this.changePwd.errorText = ''
          this.changePwd.successText = ''

          await UserRepository.change_pwd(this.changePwd.oldPwd, this.changePwd.newPwd)

          this.changePwd.successText = 'Das Passwort wurde erfolgreich geändert.'
          this.changePwd.oldPwd = ''
          this.changePwd.newPwd = ''
          this.changePwd.newPwdRep = ''
        } catch (e) {
          this.changePwd.errorText = 'Das Passwort konnte nicht aktualisiert werden. Bitte prüfen Sie, ob das bisherige Passwort korrekt eingegeben wurde.'
          this.changePwd.successText = ''

          // display error
          console.log(e)
      }
      }
    }
}
</script>