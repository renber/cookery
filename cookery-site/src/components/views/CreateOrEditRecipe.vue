<!--

Shows all information of a single recipe

-->

<template>
  <div v-if="this.isLoading || this.isSaving" class="text-center">
    <b-spinner type="grow" size="sm" />
    {{ this.isLoading ? "Wird geladen" : "Wird gespeichert" }}
  </div>

  <ContentLayout v-else :actions="actions" @actionExecuted="actionExecuted">
    <template v-slot:sidebar>
      <b-form-textarea
        v-model="recipe.title"
        placeholder="Titel des Rezepts"
        rows="2"
        style="margin-bottom: 0.25em"
      ></b-form-textarea>
      <div style="width: 100%">
        <picture-input
          ref="pictureInput"
          accept="image/jpeg"
          width="250"
          height="250"
          :zIndex=0
          size="5"
          button-class="btn btn-secondary"
          :prefill="recipe.image_url"
          :prefillOptions="{fileType: 'jpg', mediaType: 'image/jpeg'}"
          :custom-strings="{
            upload: '',
            drag: 'Bild-Datei hierher ziehen oder klicken zum Auswählen',
            change: 'Bild ersetzen',
            remove: 'Bild entfernen'
          }"
          @change="onImageChanged">
        </picture-input>
      </div>
      <b-input-group>
        <b-form-input
          v-model="recipe.portion_size"
          type="number"
          min="0"
          number
        />
        <b-input-group-append>
          <b-form-input v-model="recipe.portion_text"> </b-form-input>
        </b-input-group-append>
      </b-input-group>
      <h3>Zutaten</h3>
      <SlickList lockAxis="y" v-model="recipe.ingredients" :useDragHandle="true" tag="div" helperClass="dragged-element">
        <SlickItem v-for="(ingredient, index) in recipe.ingredients" :index="index" :key="ingredient._uid" tag="div">
          <IngredientInput :ingredientEntry="ingredient" @delete="deleteIngredient" />
        </SlickItem>
      </SlickList>
      <b-badge variant="success" href="#" @click="addIngredient" style="text-decoration: none">
        <b-icon-plus /> Zutat
      </b-badge>
      &nbsp;
      <b-badge variant="secondary" href="#" @click="addCaption" style="text-decoration: none">
        <b-icon-plus /> Überschrift
      </b-badge>
      <h3>Kategorien</h3>
      <b-form-tags
        id="category-tags"
        ref="categoryTags"
        separator=""
        placeholder="Kategorien hinzufügen"
        style="background-color:#32251b; border: none"
        v-model="recipe.tags">
      <template v-slot="{tags, removeTag}">
        <b-form-tag
            v-for="tag in tags"
            @remove="removeTag(tag)"
            :key="tag"
            :title="tag"
            :style="{'font-size': '11pt', 'background-color': getTagColor(tag)}"
            class="mr-1"
          >{{ tag }}</b-form-tag>
        <autocomplete ref="tagSearchField" @submit="addTag" :search="searchTag" :debounceTime="250" placeholder="Kategorie hinzufügen..." style="margin-top:0.5em">
        </autocomplete>
      </template>
      </b-form-tags>
      <small style="line-height: 1">Tipp: Geben Sie einen <strong>Doppelpunkt</strong> ein, um alle existierenden Oberkategorien zu sehen</small>
    </template>

    <template v-slot:content>
      <b-container>
        <b-row>
          <b-col>
            <b-alert :show="showAlert" dismissible fade variant="danger"> {{ errorMessage }} </b-alert>
            <h3>Zubereitung</h3>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            Geben Sie die Zubereitungsschritte hier ein. Nutzen Sie <strong>Leerzeilen</strong>
            zur Abtrennung der einzelnen Schritte.
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-textarea
              v-model="recipe.procedure"
              rows="15"
              placeholder=""
            ></b-form-textarea>
          </b-col>
        </b-row>
        <b-row class="mt-2">
          <b-col>
            <h3>Kommentare</h3>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-textarea
              v-model="recipe.comments"
              rows="6"
              placeholder=""
            ></b-form-textarea>
          </b-col>
        </b-row>
      </b-container>
    </template>
  </ContentLayout>
</template>

<script>
import ContentLayout from "components/layout/ContentLayout.vue"
import IngredientInput from "components/layout/IngredientInput.vue"
import RecipeRepository from "src/repo/RecipeRepository"
import TagRepository from 'src/repo/TagRepository'

import autocomplete from '@trevoreyre/autocomplete-vue'
import { SlickList, SlickItem } from 'vue-slicksort'
import PictureInput from 'vue-picture-input'
import "src/assets/css/imgoverlay.css"

import TagUtils from 'src/utils/tag-utils'

import { BAlert } from 'bootstrap-vue'

export default {
  name: "CreateOrEditRecipe",
  components: {
    ContentLayout,
    BAlert,
    IngredientInput,
    PictureInput,
    SlickList,
    SlickItem,
    autocomplete
  },
  props: {
    editRecipeId: null,
    groupName: null
  },
  data: () => {
    return {
      isLoading: false,
      isSaving: false,
      showAlert: false,
      errorMessage: null,
      actions: [
        {
          id: "save",
          title: 'Speichern',
          variant: "success",
          icon: "check2"
        },
        {
          id: "cancel",
          variant: "danger",
          title: 'Abbrechen',
          icon: "x-square"
        },
      ],
      hasImageToUpload: false,
      imageData: null,
      recipe: {
        id: null,
        title: "",
        portion_size: 1,
        portion_text: "Portion(en)",
        ingredients: [],
        comments: "",
        tags: [],
        procedure: "",
      },
    };
  },
  mounted() {
    if (this.editRecipeId) {
      this.fetch(this.editRecipeId)
    } else {
      // this.addIngredient();
    }
  },
  methods: {
    async fetch(recipeId) {
      // load the given recipe to edit
      try {
        this.isLoading = true

        const { data } = await RecipeRepository.get(recipeId)
        this.recipe = data
        this.recipe.procedure = this.recipe.steps.join("\n\n")
      } catch (error) {
        // TODO
        console.log(error);
      } finally {
        this.isLoading = false
      }
    },
    addIngredient() {
      this.recipe.ingredients.push({
        _uid: new Date().getTime(),
        is_caption: false
      });
    },
    addCaption() {
      this.recipe.ingredients.push({
        _uid: new Date().getTime(),
        is_caption: true
      });
    },
    deleteIngredient(ingredient) {
      const idx = this.recipe.ingredients.indexOf(ingredient);
      if (idx > -1) {
        console.log("delete at idx " + idx);
        this.recipe.ingredients.splice(idx, 1);
      }
    },
    onImageChanged (image) {
      if (image) {
        this.hasImageToUpload = true
        this.imageData = image
      } else {
        // TODO: FileReader APi not supported
      }
    },
    addTag (value) {
      if (!value) {
        value = this.$refs.tagSearchField.value
      }

      if (value.endsWith(':')) {
        this.$refs.tagSearchField.value = value
        // search for all tags of this group
        this.$refs.tagSearchField.core.updateResults(value)
      } else {
        this.$refs.categoryTags.addTag(value.toLowerCase())
        this.$refs.tagSearchField.value = ''
      }
    },
    async searchTag (input) {
      if (input.length < 1) return []

      if (input === ':') {
         // if a single colon is entered, show existing categories
         const { data } = await TagRepository.listCategories(this.groupName)
         return data.categories.map(x => x.name + ':')
      }
      const { data } = await TagRepository.search(input)
      return data.tags
    },
    getTagColor (value) {
      return TagUtils.getTagColor(value)
    },
    actionExecuted (actionId) {
      switch(actionId) {
        case "save": this.save(); break;
        case "cancel": this.cancel(); break;
      }
    },
    showError (message) {
      this.errorMessage = message
      this.showAlert = true
    },
    hideError () {
      this.showAlert = false
    },
    async save() {
      try {
        this.hideError()
        this.isSaving = true

        let recipeData = {
          title: this.recipe.title,
          group: this.groupName,
          portion_size: this.recipe.portion_size,
          portion_text: this.recipe.portion_text,
          ingredients: [],
          tags: this.recipe.tags,
          steps: this.recipe.procedure.split("/\r?\n//\r?\n/"),
          comments: this.recipe.comments
        };

        for (let ing of this.recipe.ingredients) {
          recipeData.ingredients.push({
            is_caption: ing.is_caption,
            quantity: ing.quantity,
            unit: ing.unit,
            comment: ing.comment,
            ingredient_id: ing.ingredient.id,
          });
        }

        try {
          const imgfile = this.$refs.pictureInput.file

          if (this.recipe.id) {
            // recipe already exists -> save changes
            await RecipeRepository.update(this.recipe.id, recipeData);

            if (this.hasImageToUpload) {
              await RecipeRepository.uploadRecipeImage(this.recipe.id, imgfile)
            }

            this.$router.push({
              name: this.groupName + "-recipe-details",
              params: { id: this.recipe.short_id, readableId: this.recipe.readable_id },
            });
          } else {
            // create new recipe
            const { data } = await RecipeRepository.create(recipeData);

            // upload image

            if (this.hasImageToUpload) {
              await RecipeRepository.uploadRecipeImage(data.id, imgfile)
            }

            // go to the new recipe's page
            this.$router.push({
              name: this.groupName + "-recipe-details",
              params: { id: data.short_id, readableId: data.readable_id },
            });
          }

          // TODO: upload image, if selected
        } catch (e) {
          this.showError('Das Rezept konnte nicht gespeichert werden')
          console.log("error: " + e);
        }
      } finally {
        this.isSaving = false;
      }
    },
    cancel () {
      this.$router.go(-1)
    }
  },
};
</script>

<style>
/* only works in non-scoped style */
.fileinput {
  display: none;
}
.img-preview {
  width: 100%;
}
</style>

<style scoped>
.step-number {
  color: black;
}

.dragged-element {
  font-family: Georgia, serif;
  color: white;
  background-color: #32251b;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

h1,
h2,
h3,
h4 {
  margin-top: 0.25em;
  margin-bottom: 0.25em;
}

textarea {
  width: 100%;
}
</style>