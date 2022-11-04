<template>
    <ContentLayout :actions="actions">
        <template v-slot:sidebar>
            <b-container fluid style="padding: 0">
                <b-form @submit.prevent="fetchRecipes(1)">
                    <b-form-row>
                        <b-col class="sep-header">
                            Rezepte-Filter
                        </b-col>
                    </b-form-row>

                    <b-form-row class="mt-1" >
                        <b-col>
                            <b-form-input @keydown.enter.native="form_key_handler" v-model="filter.text" type="text" placeholder="Name des Rezepts"></b-form-input>
                        </b-col>
                    </b-form-row>

                    <b-form-row class="mt-2">
                        <b-col class="sep-header">
                            Enthaltene Zutaten
                        </b-col>
                    </b-form-row>

                    <b-form-row>
                        <b-col>
                            <b-form-tag
                                    v-for="ingredient in filter.ingredients"
                                    :key="ingredient.id"
                                    :title="ingredient.name"
                                    :style="{'font-size': '11pt'}"
                                    class="mr-1 mb-1"
                                    @remove="removeIngredientFromFilter(ingredient)"
                                >{{ ingredient.name }}</b-form-tag>
                        </b-col>
                    </b-form-row>

                    <b-form-row>
                        <b-col>
                            <autocomplete ref="ingredientSearchField" :search="searchIngredient" :get-result-value="getIngredientDisplayValue" @submit="addIngredientToFilter" :debounceTime="250" autoSelect placeholder="Zutat suchen...">
                                <template v-slot:result="{ result, props }">
                                    <li v-bind="props" class="autocomplete-result">
                                        <div class="ingredient-path">
                                            {{ result.path }}
                                        </div>
                                        <div>
                                            {{ result.name }}
                                        </div>
                                    </li>
                                </template>
                            </autocomplete>
                        </b-col>
                    </b-form-row>

                    <b-form-row class="mt-2">
                        <b-col class="sep-header">
                            Kategorien
                        </b-col>
                    </b-form-row>

                    <b-form-row>
                        <b-col>
                            <div v-for="tagCategory in filter.availableTagCategories" :key="tagCategory.name" class="mt-1">
                                <b-btn-group>
                                    <b-dropdown size="sm" class="btn-tag-dropdown mr-1" lazy dropright :no-caret="tagCategory.tags.length == 0" :text="tagCategory.displayName" :style="{'font-size': '11pt'}">
                                        <b-dropdown-item-button size="sm" v-for="tag in tagCategory.tags" @click="addTagToFilter(tagCategory, tag)" :key="tag" :style="{'font-size': '11pt', 'background-color': getTagColor(tagCategory.name)}"> {{ tag }} </b-dropdown-item-button>
                                    </b-dropdown>

                                    <b-form-tag
                                        v-for="activeTag in tagCategory.activeTags"
                                        size="sm"
                                        :key="activeTag"
                                        :title="activeTag"
                                        :style="{'font-size': '11pt', 'background-color': getTagColor(tagCategory.name)}"
                                        class="mr-1"
                                        @remove="removeTagFromFilter(tagCategory, activeTag)"
                                    >{{ activeTag }}</b-form-tag>
                                </b-btn-group>
                            </div>
                        </b-col>
                    </b-form-row>

                    <hr/>
                    <b-form-row class="mt-2 text-center">
                        <b-col>
                            <b-button size="md" @click="fetchRecipes(1)" class="mr-2">Suchen</b-button>
                            <b-button size="md" @click="resetFilter">Zurücksetzen</b-button>
                        </b-col>
                    </b-form-row>
                </b-form>
            </b-container>
        </template>

        <template v-slot:content>
            <b-container >

            </b-container>

            <b-container>
                <b-row>
                    <b-col>
                        <b-button-toolbar>
                            <b-button-group>
                                <b-button size="sm" :pressed="viewStyle === 'images'" @click="swapViewStyle"> <b-icon icon="view-list" /> </b-button>
                                <b-button size="sm" :pressed="viewStyle === 'list'" @click="swapViewStyle"> <b-icon icon="list" /> </b-button>
                            </b-button-group>
                            <b-button-group class="ml-1">
                                <b-dropdown>
                                    <template #button-content>
                                        <b-icon icon="sort-down-alt" /> {{ sortOrder.activeSortOrder.description }}
                                    </template>

                                    <b-dropdown-item v-for="sortOption in sortOrder.availableSortOrders" :key="sortOption.id" @click="selectSortOption(sortOption)" :class="sortOption.id === sortOrder.activeSortOrder.id ? 'active-sort-order' : ''"> {{ sortOption.description }} </b-dropdown-item>
                                </b-dropdown>
                            </b-button-group>
                        </b-button-toolbar>
                    </b-col>
                </b-row>

                <b-row v-if="viewStyle === 'images'" class="align-self-stretch">
                    <b-col sm="12" md="6" lg="4" xl="3" v-for="recipe in recipes" :key="recipe.id" class="mt-1">
                        <PreviewTile :recipe="recipe" imgHeight="100px" />
                    </b-col>
                </b-row>
                <b-row v-else>
                    <b-col cols="12" v-for="recipe in recipes" :key="recipe.id" class="mt-1">
                        <router-link :to="{ name: recipe.group + '-recipe-details', params: {id: recipe.short_id, readableId: recipe.readable_id } }" class="a">
                            {{ recipe.title }}
                        </router-link>
                    </b-col>
                </b-row>
                <b-row v-if="!isLoading && recipes.length === 0">
                    <b-col class="text-center">Es wurden keine Ergebnisse gefunden.</b-col>
                </b-row>
                <b-row>
                    <b-col class="mt-1">
                        <b-pagination
                            align="center"
                            v-model="pagination.currentPage"
                            :total-rows="pagination.totalElementCount"
                            :per-page="pagination.elementsPerPage"
                            @change="pageChanged"
                            first-number
                            last-number
                        />
                    </b-col>
                </b-row>
                 <b-row class="text-center" v-if="isLoading">
                    <b-col>
                        <b-spinner variant="primary" type="grow" />
                        Rezepte werden geladen...
                    </b-col>
                </b-row>
            </b-container>
        </template>
    </ContentLayout>
</template>

<script>
import RecipeRepository from 'src/repo/RecipeRepository'
import IngredientRepository from 'src/repo/IngredientRepository'
import TagRepository from 'src/repo/TagRepository'

import ContentLayout from 'components/layout/ContentLayout.vue'
import PreviewTile from 'components/layout/PreviewTile.vue'

import TagUtils from 'src/utils/tag-utils'

import autocomplete from '@trevoreyre/autocomplete-vue'
import 'src/assets/css/autocomplete-narrow-style.css'

export default {
  name: 'Recipes',
  components: {
      ContentLayout,
      PreviewTile,
      autocomplete
  },
  props: {
    groupName: null,
  },
  data: (instance) => {
    return {
      isLoading: false,
      viewStyle: "images",
      actions: [
        {
            id: "new",
            variant: "primary",
            title: 'Neues Rezept anlegen',
            icon: "file-earmark-plus",
            to: { name: instance.groupName+'-recipe-new' }
        },
        {
            id: "share",
            title: 'Suchergebnisse teilen',
            icon: "share"
        }
      ],
      filter: {
          text: "",
          ingredients: [],
          availableTagCategories: []
      },
      sortOrder: {
        activeSortOrder: "",
        availableSortOrders: [
            {
                id: "latest_first",
                description: "Neueste Rezepte zuerst"
            },
            {
                id: "oldest_first",
                description: "Älteste Rezepte zuerst"
            },
            {
                id: "alphabetical_asc",
                description: "Alphabetisch aufsteigend sortieren"
            }
            ,{
                id: "alphabetical_desc",
                description: "Alphabetisch absteigend sortieren"
            }
        ]
      },
      pagination: {
          currentPage: 1,
          elementsPerPage: 12,
          totalElementCount: 0,
      },
      recipes: [],
    };
  },
  created () {
    this.sortOrder.activeSortOrder = this.sortOrder.availableSortOrders[0]
  },
  mounted () {
    this.fetchAvailableTagCategories()
    this.fetchRecipes(1)
  },
  methods: {
      async fetchRecipes (page) {
          try {
              this.isLoading = true

              let ingredient_list = []
              this.filter.ingredients.forEach(ing => {
                  ingredient_list.push(ing.id)
              })

              let tag_list = []
              this.filter.availableTagCategories.forEach(tc => {
                  tc.activeTags.forEach(t => {
                      if (tc.name === '$ungrouped') {
                        tag_list.push(t)
                      } else {
                        tag_list.push(tc.name + ':' + t)
                      }
                  })
              })

              const { data } = await RecipeRepository.list(this.groupName, page, this.pagination.elementsPerPage, this.filter.text, this.sortOrder.activeSortOrder.id, ingredient_list, tag_list)
              if (this.pagination.totalElementCount != data.recipe_count) {
                this.pagination.totalElementCount = data.recipe_count
              }
              this.recipes = data.recipes
          } finally {
              this.isLoading = false;
          }
      },
      async fetchAvailableTagCategories () {
          const { data } = await TagRepository.listCategories(this.groupName)

          data.categories.forEach(element => {
            element.activeTags = []

            if (element.name === '$ungrouped') {
                element.displayName = 'sonstige'
            } else {
                element.displayName = element.name
            }
          });

          this.filter.availableTagCategories = data.categories
      },
      // eslint-disable-next-line no-unused-vars
      pageChanged (page) {
          this.fetchRecipes(page)
      },
      swapViewStyle () {
          if (this.viewStyle === 'list') {
              this.viewStyle = 'images'
          } else {
              this.viewStyle = 'list'
          }
      },
      selectSortOption(sortOption) {
          this.sortOrder.activeSortOrder = sortOption
          this.fetchRecipes(this.pagination.currentPage)
      },
      resetFilter () {
          this.filter.text = ''
          this.ingredients = []
          this.fetchAvailableTagCategories().then(() => this.fetchRecipes(1))
      },
      async searchIngredient (input) {
         if (input.length < 1) { return [] }
         const { data } = await IngredientRepository.search(input)
         return data
      },
      getIngredientDisplayValue (ingredient) {
            return ingredient.name
      },
      addIngredientToFilter (ingredient) {
          this.filter.ingredients.push(ingredient)
          this.$refs.ingredientSearchField.setValue('')
      },
      removeIngredientFromFilter (ingredient) {
        this.filter.ingredients.splice(this.filter.ingredients.indexOf(ingredient), 1)
      },
      getTagColor (value) {
          return TagUtils.getTagColor(value)
      },
      addTagToFilter(category, tag) {
        category.tags.splice(category.tags.indexOf(tag), 1)
        category.activeTags.push(tag)
      },
      removeTagFromFilter(category, tag) {
        category.activeTags.splice(category.activeTags.indexOf(tag), 1)
        category.tags.push(tag)
      },
      form_key_handler(event) {
          // search on pressing Enter
          if (event.which === 13) {
            this.fetchRecipes(1)
          }
      }
  }
}
</script>

<style scoped>
    .sep-header {
        font-family: Arvo, serif;
        letter-spacing: -1px;
        font-weight: bold;
        font-size: 1.17em;
        color: #fff;
    }

    .active-sort-order {
        background-color: #6c757d;
    }

    .ingredient-path {
        line-height: 1;
        font-size: 10px
    }
    .autocomplete-result {
        color: black
    }
    hr {
        background-color: white;
        margin-left: 25%;
        margin-right: 25%;
    }
</style>

<style>
    .btn-tag-dropdown .dropdown-menu {
        padding: 0 0;
    }

    .dropdown-item {
        text-decoration: none;
    }

    .btn-tag-dropdown .dropdown-item {
        color: white;
        padding: 0 0.5rem;
    }

    .dropdown-item:hover, .dropdown-item:focus {
        background-color: orange;
    }
</style>