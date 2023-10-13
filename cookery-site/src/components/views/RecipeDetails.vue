<!--

Shows all information of a single recipe

-->

<template>
  <div v-if="this.isLoading" class="text-center">
    <b-spinner type="grow" size="sm" />Wird geladen
  </div>

  <ContentLayout v-else :actions="isCooking ? cookingActions : actions" @actionExecuted="actionExecuted">
    <template v-slot:sidebar>

      <b-container id="sidebar-container">
        <b-row no-gutters>
          <b-col class="text-center">
            <h2 id="recipe-title">{{ recipe.title }}</h2>
          </b-col>
        </b-row>
        <b-row>
          <b-col class="text-center">
            <img :src="recipe.image_url" id="main-image" />
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="1"></b-col>
          <b-col cols="10" class="text-center">
              <EditableSpinButtonGroup id="spinner-portion-size" v-model="wantedPortionSize" :title="recipe.portion_text"></EditableSpinButtonGroup>
          </b-col>
          <b-col cols="1"></b-col>
        </b-row>
        <b-row>
          <b-col>
            <h3>Zutaten</h3>
          </b-col>
        </b-row>
        <b-row>
          <!-- two columns for xs -->
            <b-col cols="6" sm="12" lg="12" xl="12" v-for="ingredient in recipe.ingredients" :key="ingredient.ingredient.id">
              <div v-if="ingredient.is_caption">
                 <strong> {{ ingredient.comment }} </strong>
              </div>
              <div v-else style="margin-left:12px">
                {{ (ingredient.quantity * wantedPortionSize / recipe.portion_size) | formatIngredientAmount }} {{ ingredient.unit }}
                <a :href="ingredient.ingredient.associated_recipe_url | getPublicUrl">
                  {{ ingredient | getIngredientDisplayText(ingredient.quantity * wantedPortionSize / recipe.portion_size) }}
                </a>
                {{ ingredient.comment | inBrackets }}
              </div>
            </b-col>
        </b-row>
        <b-row v-if="recipe.tags.length > 0">
          <b-col>
            <h3>Kategorien</h3>
          </b-col>
          <b-container>
            <b-row no-gutters>
              <b-col cols="12">
                <tag-view :tags="recipe.tags" />
              </b-col>
            </b-row>
          </b-container>
        </b-row>
      </b-container>
    </template>

    <template v-slot:content>
      <b-container>
         <b-row>
          <b-col>
            <h3>Zubereitung</h3>
          </b-col>
        </b-row>

        <b-row v-for="(step, index) in recipe.steps" :key="step" :class="activeStepIndex == index ? 'active-step' : ''" @click="activateStep(index)">
          <b-col xs="2" sm="2" md="1" lg="1" xl="1">
            <div class="text-left">
              <h2 class="step-number">{{ index + 1 | formatStepNumber }}</h2>
            </div></b-col>

          <b-col style="padding-top: 10px"> {{ step }}

            <!-- Button Bar for active step -->
            <b-button-toolbar  v-if="isCooking && activeStepIndex == index" style="padding-bottom:5px">
              <b-button-group v-if="speechSynthAllowed" class="mr-1">
                <b-button size="sm" @click="tellStep(index)" v-on:click.stop title="Anweisungen wiederholen" v-b-tooltip.hover.bottom> <b-icon icon="arrow-repeat" /> </b-button>
              </b-button-group>
              <b-button-group class="mr-1">
                <b-button size="sm" :disabled="index == 0" @click="prevStep" v-on:click.stop title="Vorheriger Schritt" v-b-tooltip.hover.bottom> <b-icon icon="arrow-left" /> </b-button>
                <b-button size="sm" :disabled="index == recipe.steps.length - 1" @click="nextStep" v-on:click.stop title="Nächster Schritt" v-b-tooltip.hover.bottom> <b-icon icon="arrow-right" /> </b-button>
              </b-button-group>

              <b-input-group size="sm" v-if="speechControlAllowed">
                <template #prepend>
                  <b-input-group-text><b-icon icon="mic" /></b-input-group-text>
                </template>
                <template #append>
                  <b-input-group-text><b-icon icon="question-circle" /></b-input-group-text>
                </template>
                <b-form-input readonly value="Hört zu..."></b-form-input>
              </b-input-group>
           </b-button-toolbar>
          </b-col>

        </b-row>
        <b-row class="mt-2" v-if="recipe.comments">
          <b-col>
            <h3>Kommentare</h3>
          </b-col>
        </b-row>
        <b-row v-if="recipe.comments">
          <b-col>
            <div style="white-space: break-spaces;">{{ recipe.comments }}</div>
          </b-col>
        </b-row>
      </b-container>
    </template>
  </ContentLayout>
</template>

<script>
import ContentLayout from "components/layout/ContentLayout.vue"
import RecipeRepository from "src/repo/RecipeRepository"
import TagView from "components/layout/TagView.vue"
import IngredientUtils from 'src/utils/ingredient-utils'
import EditableSpinButtonGroup from "components/layout/EditableSpinButtonGroup.vue"
import UrlUtils from "src/utils/url-utils"
import { formatCommonFraction } from 'src/utils/number-utils'

import { speechSynth } from 'src/services/SpeechSynth'
// import { speechListener } from 'src/services/SpeechListener'

export default {
  name: "RecipeDetails",
  components: {
    ContentLayout,
    TagView,
    EditableSpinButtonGroup
  },
  props: {
    groupName: null
  },
  data: () => {
    return {
      isLoading: false,
      actions: [
        {
            id: "startCooking",
            variant: "primary",
            title: 'Zubereitung beginnen',
            icon: "play"
        },
        {
            id: "edit",
            title: 'Rezept bearbeiten',
            icon: "pencil-square"
        },
        {
            id: "share",
            title: 'Rezept teilen',
            icon: "share"
        }
      ],
      cookingActions: [
        {
            id: "stopCooking",
            variant: "primary",
            title: 'Zubereitung beenden',
            icon: "stop"
        },
        {
            id: "speechSynthToggle",
            hidden: false,
            variant: "danger",
            title: 'Sprachausgabe aktivieren',
            icon: "volume-mute"
        }/*,
        {
            id: "speechControlToggle",
            variant: "danger",
            title: 'Sprachsteuerung aktivieren',
            icon: "mic-mute"
        } */
      ],
      speechSynthToggleBtn: null,
      //speechControlToggleBtn: null,
      recipe: {},
      wantedPortionSize: 4,
      isCooking: false,
      activeStepIndex: -1,
      speechSynthAllowed: false,
      speechControlAllowed: false
    };
  },
  computed: {
    recipeSiteId() {
      return this.$router.currentRoute.params.id;
    },
  },
  created() {
    this.fetch();

    this.speechSynthToggleBtn = this.cookingActions[1]
    this.speechControlToggleBtn = this.cookingActions[2]
    this.updateButtons()
  },
  beforeDestroy () {
    // stop speech recognition, if it is running
    // speechListener.stop()
  },
  methods: {
    async fetch() {
      try {
        this.isLoading = true;
        // TODO: handle errors (e.g. recipe does not exist)
        const { data } = await RecipeRepository.get(this.recipeSiteId);
        this.recipe = data;
        this.wantedPortionSize = this.recipe.portion_size
        const groupName = this.recipe.group

        // push the "correct" url
          this.$router.replace({
            name: groupName + "-recipe-details",
            params: {
              id: this.recipe.short_id,
              readableId: this.recipe.readable_id,
            },
          }).catch(err => {
            if (err.name !== 'NavigationDuplicated') {
              console.log(err)
            }
          });
      } catch (e) {
        // TODO: check for not found or other error
        // forward to 404 page (but keep the current url)
        console.log(e)
        this.$router.push({ name: "404", params: { 0: this.$route.path } });
      } finally {
        this.isLoading = false;
      }
    },
    actionExecuted (actionId) {
      if (actionId === "edit") {
        this.edit()
      }
      if (actionId === "startCooking") {
        this.startCooking()
      }
      if (actionId === "stopCooking") {
        this.stopCooking()
      }
      if (actionId === "speechSynthToggle") {
        this.speechSynthAllowed = !this.speechSynthAllowed
        this.updateButtons()
      }
      /*
      if (actionId === "speechControlToggle") {
        this.speechControlAllowed = !this.speechControlAllowed
        this.updateButtons()

        if (this.speechControlAllowed) {
          this.listenForCommands()
        } else {
          this.speechListener.stop()
        }
      } */
    },
    startCooking () {
      this.activeStepIndex = 0
      this.updateButtons()

      this.isCooking = true
    },
    stopCooking () {
      this.activeStepIndex = -1
      this.isCooking = false

      // this.speechListener.stop()
    },
    listenForCommands() {
      /* speechListener.init()
      speechListener.listen() */
    },
    edit () {
      this.$router.push({
        name: this.groupName + "-recipe-edit",
        params: { id: this.recipe.short_id, readableId: this.recipe.readable_id },
      });
    },
    activateStep (stepIndex) {
      if (!this.isCooking) return

      if (this.activeStepIndex !== stepIndex) {
        this.activeStepIndex = stepIndex

        if (this.speechSynthAllowed) {
          this.tellStep(this.activeStepIndex)
        }
      }
    },
    tellStep (stepIndex) {
      speechSynth.say(this.recipe.steps[stepIndex])
    },
    prevStep () {
      if (this.activeStepIndex > 0) {
        this.activateStep(this.activeStepIndex - 1)
      }
    },
    nextStep () {
      if (this.activeStepIndex < this.recipe.steps.length - 1) {
        this.activateStep(this.activeStepIndex + 1)
      }
    },
    updateButtons () {
      if (this.isCooking) {
        this.speechSynthToggleBtn.title = this.speechSynthAllowed ? 'Sprachausgabe aktiv' : 'Sprachausgabe inaktiv'
        this.speechSynthToggleBtn.variant = this.speechSynthAllowed ? 'success' : 'danger'
        this.speechSynthToggleBtn.icon = this.speechSynthAllowed ? 'volume-up' : 'volume-mute'

        /* this.speechControlToggleBtn.title = this.speechControlAllowed ? 'Sprachsteuerung aktiv' : 'Sprachsteuerung inaktiv'
        this.speechControlToggleBtn.variant = this.speechControlAllowed ? 'success' : 'danger'
        this.speechControlToggleBtn.icon = this.speechControlAllowed ? 'mic' : 'mic-mute' */
      }
    }
  },
  filters: {
    inBrackets: function (value) {
        if (value) {
            return '(' + value + ')'
        } else {
          return ''
        }
    },
    formatIngredientAmount: function (value) {
      return formatCommonFraction(value)
    },
    getIngredientDisplayText: function (ingredient, quantity) {
      return IngredientUtils.getIngredientDisplayText(ingredient, quantity)
    },
    formatStepNumber: function (number) {
      return `${number}`.padStart(2, '\xa0') // pad with non-breaking spaces
    },
    getPublicUrl (relativeUrl) {
      if (relativeUrl) {
        return UrlUtils.getPublicUrl(relativeUrl)
      } else {
        return null
      }
    }
},
};
</script>

<style scoped>

#main-image {
  width: 100%;
  max-width: 250px;
  max-height: 250px;
  object-fit: cover;
  margin-top: 0.25em;
  margin-bottom: 0.25em;
}

#sidebar-container {
  padding-left: 0;
  padding-right: 0;
}

/*
.step-number {
  color: black;
}*/

.active-step {
  background: #32251b;
  color: white;
}

h1,
h2,
h3,
h4 {
  margin-top: 0.25em;
  margin-bottom: 0em;
}
</style>