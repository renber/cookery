<!-- Configfuration view which allows to create/edit ingredients and categories -->

<template>
  <b-container>
    <b-row v-for="group in groups" :key="group.id" no-gutters>
      <b-col>
        <IngredientGroupTreeNode :group="group" @add-ingredientgroup="showModalAddIngredientGroup" @add-ingredient="showModalAddIngredient" @edit-ingredient="showModalEditIngredient" />
      </b-col>
    </b-row>
    <b-row no-gutters>
       <b-col>
         <b-container>
           <b-row>
             <b-col>
               <b-button-group>
                 <b-button v-on:click="showModalAddIngredientGroup(null)"> <b-icon-folder-plus /> Obergruppe hinzufügen </b-button>
               </b-button-group>
             </b-col>
           </b-row>
         </b-container>
       </b-col>
    </b-row>

    <b-modal id="modal-add-ingredientgroup" title="Zutatengruppe hinzufügen" @ok="modalOkAddIngredientGroup" cancel-title="Abbrechen">
      <b-form @submit.prevent="modalSubmitAddIngredientGroup" autocomplete="off">
        <b-form-group
          v-if="modals.addIngredientGroup.parentNode"
          label="Übergeordnete Gruppe:"
          label-for="parent-input"
          description=""
        >
          <b-form-input
            id="parent-input"
            type="text"
            :value="modals.addIngredientGroup.parentNode.group.name"
            plaintext
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="name-group"
          label="Name:"
          label-for="name-input"
        >
          <b-form-input
            id="name-input"
            v-model="modals.addIngredientGroup.name"
            type="text"
            placeholder="Name der Gruppe eingeben"
            required
          ></b-form-input>
        </b-form-group>

        <div v-if="modals.addIngredientGroup.errorMessage" class="error-message">
          {{ modals.addIngredientGroup.errorMessage }}
        </div>

        <b-button hidden type="submit"></b-button>
      </b-form>
    </b-modal>

    <b-modal id="modal-add-ingredient" :title="modals.addIngredient.editId ? 'Zutat bearbeiten' : 'Zutat hinzufügen'" @ok="modalOkAddIngredient" cancel-title="Abbrechen">      
      <b-form @submit.prevent="modalSubmitAddIngredient" autocomplete="off">
          <b-form-group
            v-if="modals.addIngredient.parentNode"
            label="Gruppe:"
            label-for="parent-input"
            description=""
          >
            <b-form-input
              id="parent-input"
              type="text"
              :value="modals.addIngredient.parentNode.group.name"
              plaintext
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="name-group"
            label="Zutat (Pluralform):"
            label-for="name-input"
          >
            <b-form-input
              id="name-input"
              v-model="modals.addIngredient.name"
              type="text"
              placeholder="Name der Zutat eingeben (Pluralform)"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="singular-group"
            label="Singular:"
            label-for="singular-input"
          >
            <b-form-input
              id="singular-input"
              v-model="modals.addIngredient.singular"
              type="text"
              placeholder="Singularform, falls vorhanden/gewünscht"              
            ></b-form-input>
          </b-form-group>

          <div v-if="modals.addIngredient.errorMessage" class="error-message">
            {{ modals.addIngredient.errorMessage }}
          </div>

          <b-button hidden type="submit"></b-button>
      </b-form>      
    </b-modal>
  </b-container>
</template>

<script>
import IngredientRepository from "src/repo/IngredientRepository"
import IngredientGroupTreeNode from "components/layout/IngredientGroupTreeNode"

export default {
  name: "config-ingredients",
  components: {
    IngredientGroupTreeNode
  },
  data: () => {
    return {
      isLoading: false,
      groups: [],
      modals: {
        addIngredientGroup: {
          editId: null, // ID of the ingredient if editing
          parentNode: null,
          name: '',
          singular: '',
          errorMessage: null
        },
        addIngredient: {
          parentNode: null,
          name: '',
          errorMessage: null
        }
      }
    };
  },
  mounted() {
    this.fetchTopLevelGroups();
  },
  methods: {
    async fetchTopLevelGroups() {
      try {
      this.groups = []
        this.isLoading = true
        // TODO: handle errors (e.g. recipe does not exist)
        const { data } = await IngredientRepository.listTopLevelGroups()
        this.groups = data
      } catch (e) {
        // display error
      } finally {
        this.isLoading = false;
      }
    },
    showModalAddIngredientGroup(parentNode) {
      this.modals.addIngredientGroup.parentNode = parentNode
      this.modals.addIngredientGroup.name = ''
      this.modals.addIngredientGroup.errorMessage = null
      this.$bvModal.show('modal-add-ingredientgroup');
    },
    showModalAddIngredient(parentNode) {
      if (parentNode != null) {
        this.modals.addIngredient.editId = null
        this.modals.addIngredient.parentNode = parentNode
        this.modals.addIngredient.name = ''
        this.modals.addIngredient.singular = ''
        this.modals.addIngredient.errorMessage = null
        this.$bvModal.show('modal-add-ingredient');
      }
    },
    showModalEditIngredient(parentNode, ingredient) {
      if (ingredient != null) {    
        this.modals.editIngredient = ingredient
        this.modals.addIngredient.editId = ingredient.id
        this.modals.addIngredient.parentNode = parentNode
        this.modals.addIngredient.name = ingredient.name
        this.modals.addIngredient.singular = ingredient.singular
        this.modals.addIngredient.errorMessage = null
        this.$bvModal.show('modal-add-ingredient');
      }
    },
    modalOkAddIngredientGroup(bvModalEvt) { // eslint-disable-line no-unused-vars      
      // Prevent modal from closing
      bvModalEvt.preventDefault()

      this.modalSubmitAddIngredientGroup()
    },
    modalSubmitAddIngredientGroup() {
      this.createNewGroup(this.modals.addIngredientGroup.parentNode, this.modals.addIngredientGroup.name)
    },
    modalOkAddIngredient(bvModalEvt) { // eslint-disable-line no-unused-vars
      // Prevent modal from closing
      bvModalEvt.preventDefault()

      this.modalSubmitAddIngredient()
    },
    modalSubmitAddIngredient() {
      if (this.modals.addIngredient.editId) {
        if (this.updateIngredient(this.modals.addIngredient.parentNode, this.modals.addIngredient.editId, this.modals.addIngredient.name, this.modals.addIngredient.singular))
        {
            this.modals.editIngredient.name = this.modals.addIngredient.name
            this.modals.editIngredient.singular = this.modals.addIngredient.singular
        }
      } else {
        this.createNewIngredient(this.modals.addIngredient.parentNode, this.modals.addIngredient.name, this.modals.addIngredient.singular)
      }
    },
    async createNewGroup(parentNode, name) {
      let newGroup = {                        
        name: name                
      }

      if (parentNode) {
        newGroup.parent_group_id = parentNode.group.id
      }      

      try {
          const { data } = await IngredientRepository.createGroup(newGroup)

          if (parentNode == null) {
            this.groups.push(data)
          } else {
            parentNode.group.has_child_groups = true
            
            if (parentNode.wasLoaded) {              
              parentNode.childGroups.push(data)        
            } else {
              parentNode.expand()
            }
          }

          this.$bvModal.hide('modal-add-ingredientgroup')
      } catch (e) {
        this.modals.addIngredientGroup.errorMessage = 'Die Gruppe konnte nicht angelegt werden'

        // display error
        console.log(e)
      }
    },
    async createNewIngredient(parentNode, name, singular) {
      let newIngredient = {        
        group_id: parentNode.group.id,
        name: name,
        singular: singular
      }

      try {
          this.modals.addIngredient.errorMessage = null

          const { data } = await IngredientRepository.createIngredient(newIngredient)

          parentNode.group.has_ingredients = true

          if (parentNode.wasLoaded) {
            parentNode.ingredients.push(data)            
          } else {
            parentNode.expand()
          }

          this.$bvModal.hide('modal-add-ingredient')
      } catch (e) {
        this.modals.addIngredient.errorMessage = 'Die Zutat konnte nicht angelegt werden'
        // display error
        console.log(e)
      }      
    },
    async updateIngredient(parentNode, ingredientId, name, singular) {
      let updatedIngredient = {        
        group_id: parentNode.group.id,
        name: name,
        singular: singular
      }

      try {
          this.modals.addIngredient.errorMessage = null

          await IngredientRepository.updateIngredient(ingredientId, updatedIngredient)          

          this.$bvModal.hide('modal-add-ingredient')
          return true          
      } catch (e) {
        this.modals.addIngredient.errorMessage = 'Die Zutat konnte nicht aktualisiert werden'
        // display error
        console.log(e)
        return false
      }      
    }
  },
};
</script>

<style scoped>

.error-message {
  color: darkred
}

</style>