<!-- A component which represents a single IngredientGroup and
 which can be expanded if child groups are present -->

<template>
  <b-container class="sub-container">
    <b-row
      no-gutters
      @mouseenter="isSelected = true"
      @mouseleave="isSelected = false"
    >
      <b-col cols="4">
        <b-button
          v-if="isExpanded"
          v-on:click="collapse"
          variant="outline-secondary"
        >
          <b-icon-folder2-open /> {{ group.name }}
        </b-button>
        <b-button v-else v-on:click="expand" variant="outline-secondary">
          <b-icon-folder
            v-if="group.has_ingredients || group.has_child_groups"
          />
          <b-icon-folder-x v-else />
          {{ group.name }}
        </b-button>
      </b-col>
      <b-col v-if="isSelected">
        <b-button-toolbar>
          <b-button-group class="mx-1">
            <b-button
              v-on:click="raiseAddIngredient()">
              <b-icon-node-plus /> Zutat hinzufügen
            </b-button>
          </b-button-group>
          <b-button-group class="mx-1">
            <b-button
              v-on:click="raiseAddIngredientGroup()">
              <b-icon-folder-plus /> Gruppe hinzufügen
            </b-button>
          </b-button-group>
        </b-button-toolbar>
      </b-col>
    </b-row>
    <b-row v-if="isExpanded" no-gutters>
      <b-container>
        <b-row v-for="childgroup in childGroups" :key="childgroup.id">
          <ingredient-group-tree-node
            :group="childgroup"
            @add-ingredient="forwardAddIngredientEvent"
            @add-ingredientgroup="forwardAddIngredientGroupEvent"
            @edit-ingredient="forwardEditIngredientEvent"
          />
        </b-row>
        <b-row v-for="ingredient in ingredients" :key="ingredient.id">
          <b-container>
            <b-row no-gutters align-v="center">               
              <b-col> <b-icon-dot /> {{ ingredient.name }} {{ ingredient.singular ? (' / ' + ingredient.singular) : ''  }} </b-col>
              <b-col>
                <b-button-toolbar>
                  <b-button-group class="mx-1">
                    <b-button
                      v-on:click="raiseEditIngredient(ingredient)">
                      <b-icon-pencil-square /> Bearbeiten
                    </b-button>
                  </b-button-group>                
                </b-button-toolbar>
              </b-col>
            </b-row>
          </b-container>
        </b-row>
      </b-container>
    </b-row>
  </b-container>
</template>

<script>
import IngredientRepository from "src/repo/IngredientRepository";

export default {
  name: "IngredientGroupTreeNode",
  props: {
    group: Object,
  },
  data: () => {
    return {
      isLoading: false,
      wasLoaded: false,
      isExpanded: false,
      isSelected: false,
      childGroups: [],
      ingredients: []
    };
  },
  methods: {
    expand() {
      if (this.isExpanded) {
        return;
      }

      if (this.wasLoaded) {
        this.isExpanded = true;
      } else {
        if (this.group.has_child_groups || this.group.has_ingredients) {          
          this.fetchChildGroups().then((this.isExpanded = true));
        }
      }

      this.isSelected = true;
    },
    collapse() {
      this.isExpanded = false;
      this.isSelected = false;
    },
    async fetchChildGroups() {
      try {
        this.isLoading = true;
        // TODO: handle errors (e.g. recipe does not exist)
        const { data } = await IngredientRepository.getGroup(this.group.id);

        this.ingredients = data.ingredients        

        this.childGroups = data.child_groups
      } catch (e) {
        // display error
      } finally {
        this.wasLoaded = true;
        this.isLoading = false;
      }
    },
    forwardAddIngredientGroupEvent(node) {
      this.$emit("add-ingredientgroup", node);
    },
    forwardAddIngredientEvent(node) {
      this.$emit("add-ingredient", node);
    },
    forwardEditIngredientEvent(node, ingredient) {
      this.$emit("edit-ingredient", node, ingredient);
    },
    raiseAddIngredientGroup() {
      this.$emit('add-ingredientgroup', this);
    },
    raiseAddIngredient() {
      this.$emit('add-ingredient', this);
    },
    raiseEditIngredient(ingredient) {
      this.$emit('edit-ingredient', this, ingredient);
    }
  },
};
</script>

<style scoped>
.sub-container {
  margin-bottom: 5px;
}
</style>