<template>
    <b-container v-if="editable" fluid class="pl-0 pr-0">
        <b-form-row no-gutters align-v="center">
            <b-col cols="1" align-self="center">
                <b-badge variant="danger" size="sm" href="#" @click="raiseDelete"> <b-icon-trash /> </b-badge>
            </b-col>
            <b-col v-if="!ingredientEntry.is_caption" cols="5">
                <b-form-input v-model="ingredientEntry.quantity" min="0" placeholder="Menge" type="number" />
            </b-col>
            <b-col v-if="!ingredientEntry.is_caption" cols="6">
                <b-form-input v-model="ingredientEntry.unit" placeholder="Einheit" />
            </b-col>
            <b-col v-if="ingredientEntry.is_caption" cols="10">
                <b-form-input v-model="ingredientEntry.comment" placeholder="Überschrift" />
            </b-col>
            <b-col v-if="ingredientEntry.is_caption" cols="1" align-self="center">
                <b-badge variant="success" size="sm" href="#" @click="finishEditing"> <b-icon-check /> </b-badge>
            </b-col>
        </b-form-row>
        <b-form-row v-if="!ingredientEntry.is_caption">
            <b-col>
                <autocomplete  ref="ingredientSearchField" :defaultValue="ingredientEntry.ingredient.name" :search="searchIngredient" :get-result-value="getIngredientDisplayValue" @submit="setIngredient" :debounceTime="250" autoSelect placeholder="Zutat suchen...">
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
                </autocomplete >
            </b-col>            
        </b-form-row>
        <b-form-row v-if="!ingredientEntry.is_caption">
            <b-col>
                <b-form-input v-model="ingredientEntry.comment" placeholder="Kommentar" />
            </b-col>
            <b-col v-if="!ingredientEntry.is_caption" cols="1" align-self="center">
                <b-badge variant="success" size="sm" href="#" @click="finishEditing"> <b-icon-check /> </b-badge>
            </b-col>
        </b-form-row>
    </b-container>
    <b-container v-else fluid class="pl-0 pr-0">
        <b-row no-gutters>
            <b-col v-if="ingredientEntry.is_caption" cols="11" style="cursor:move">
                <div v-handle> <strong> {{ ingredientEntry.comment }} </strong> </div>                
            </b-col>

            <b-col v-else cols="11" style="cursor:move">
                <div v-handle style="margin-left:12px"> {{ ingredientEntry.quantity }} {{ ingredientEntry.unit }} {{ ingredientEntry | getIngredientDisplayText }} {{ ingredientEntry.comment | inBrackets }}</div>
            </b-col>

            <b-col cols="1">
                <b-badge variant="secondary" size="sm" href="#" @click="edit"> <b-icon-pencil /> </b-badge>
            </b-col>
        </b-row>

    </b-container>
</template>

<script>
import IngredientRepository from 'src/repo/IngredientRepository'
import { HandleDirective } from 'vue-slicksort'

import IngredientUtils from 'src/utils/ingredient-utils'

import autocomplete from '@trevoreyre/autocomplete-vue'
import 'src/assets/css/autocomplete-narrow-style.css'

export default {
    name: 'IngredientInput',
    props: {
        ingredientEntry: Object
    },
    directives: { handle: HandleDirective },
    data: () => {
        return {
           editable: true
        }
    },
    components: {
        autocomplete
    },
    created () {
        if (!this.ingredientEntry.ingredient) {
            this.ingredientEntry.editable =  true
            this.ingredientEntry.quantity = null
            this.ingredientEntry.unit = ''
            this.ingredientEntry.comment = ''
            this.ingredientEntry.ingredient = {
                name: ''
            }
        }

        this.editable = this.ingredientEntry.editable
    },
    methods: {
        async searchIngredient (input) {
         if (input.length < 1) { return [] }
         const { data } = await IngredientRepository.search(input)

         data.push({
             id: 'create-new',
             name: 'Als neue Zutat hinzufügen'
         })

         return data
        },
        getIngredientDisplayValue (ingredient) {
            return ingredient.name
        },
        setIngredient (ingredient) {
            if (ingredient.id !== 'create-new') {
                this.ingredientEntry.ingredient = ingredient

                // this.editable = false
                // this.ingredientEntry.editable = false
            } else {
                this.$refs.ingredientSearchField.setValue('')
            }
        },
        raiseDelete () {
            this.$emit('delete', this.ingredientEntry)
        },        
        edit () {
            this.editable = true
            this.ingredientEntry.editable = true
        },
        finishEditing () {
            this.editable = false
            this.ingredientEntry.editable = false
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
        getIngredientDisplayText: function (ingredient) {
            return IngredientUtils.getIngredientDisplayText(ingredient)            
        }
    }
}
</script>

<style scoped>
    .ingredient-path {
        line-height: 1;
        font-size: 10px
    }
    .autocomplete-result {
        color: black
    }
</style>