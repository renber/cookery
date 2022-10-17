<template>
        <b-container fluid id="content">
        <b-row>            
            <b-col sm="12" >
                <h2>Willkommen bei Cookery!</h2>
            </b-col>
        </b-row>	
        <b-row>
            <b-col>
                Die neuesten Koch-Rezepte:
            </b-col>
        </b-row>
       <b-form-row>
            <b-col xs="12" sm="12" md="4" lg="2" xl="2" v-for="recipe in latestCookingRecipes" :key="recipe.id">
                <PreviewTile :recipe="recipe" imgHeight="150px" withTags="true" />                
            </b-col>
        </b-form-row>
        <b-row class="mt-2">
            <b-col>
                Die neuesten Back-Rezepte:
            </b-col>
        </b-row>
       <b-form-row>
            <b-col xs="12" sm="12" md="4" lg="2" xl="2" v-for="recipe in latestBakingRecipes" :key="recipe.id">
                <PreviewTile :recipe="recipe" imgHeight="150px" withTags="true" />                
            </b-col>
        </b-form-row>
        <b-row class="mt-2">
            <b-col>
                Die neuesten Cocktails:
            </b-col>
        </b-row>
       <b-form-row>
            <b-col xs="12" sm="12" md="4" lg="2" xl="2" v-for="recipe in latestCocktails" :key="recipe.id">
                <PreviewTile :recipe="recipe" imgHeight="150px" withTags="true" />                
            </b-col>
        </b-form-row>        
    </b-container>	
</template>

<script>

import RecipeRepository from 'src/repo/RecipeRepository'
import PreviewTile from 'components/layout/PreviewTile'

export default {
  name: 'Home',
  components: {
    PreviewTile
  },
  data: () => {
      return {
          latestCookingRecipes: [],
          latestBakingRecipes: [],
          latestCocktails: []
      }
  },
  mounted () {
      this.fetchLatestRecipes('kochen', this.latestCookingRecipes)
      this.fetchLatestRecipes('backen', this.latestBakingRecipes)
      this.fetchLatestRecipes('cocktails', this.latestCocktails)
  },
  methods: {
      async fetchLatestRecipes (groupName, targetList) {
          const { data } = await RecipeRepository.listLatest(groupName, 6)
          targetList.length = 0
          targetList.push(...data)
      }
  }
}
</script>