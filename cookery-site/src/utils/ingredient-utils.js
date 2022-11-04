
export default {

    getIngredientDisplayText (recipeIngredient, quantity = null) {
        if (quantity == null) {
            quantity = recipeIngredient.quantity
        }

        if (quantity <= 1 && !recipeIngredient.unit && recipeIngredient.ingredient.singular) {
            return recipeIngredient.ingredient.singular
        } else {
            return recipeIngredient.ingredient.name
        }
    }
}