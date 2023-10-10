
/**
 * Compares to float numbers using a sensible tolerance for ingredients and recipe amounts
 * @param f1 Number
 * @param f2 Number to compare with
 * @returns True if the numbers are considered equal in teh specified context
 */
export function compareRecipeFloat(f1: number, f2: number): boolean {
  return Math.abs(f1 - f2) < 0.001
}

export function parseCommonFraction(input: string): number {
    const slashIdx = input.indexOf('/')
    if (slashIdx === -1) {
      return Number.parseFloat(input)
    }

    const numerator = Number.parseInt(input.substring(0, slashIdx).trim())
    const denominator = Number.parseInt(input.substring(slashIdx + 1).trim())

    if (Number.isNaN(numerator) || Number.isNaN(denominator) || denominator === 0) {
      return NaN
    }

    return numerator / denominator
}

/**
 * Return a string representation of teh given number where "common" farctions (e.g. 1/2, 2/3)
 * are returned as "x/y"
 * @param value number
 * @returns textual representation of number
 */
export function formatCommonFraction(value: number): string {

    if (!value) {
      return "";
    }

    if (compareRecipeFloat(value, 1/2)) return "1/2"

    if (compareRecipeFloat(value, 1/3)) return "1/3"
    if (compareRecipeFloat(value, 2/3)) return "2/3"

    if (compareRecipeFloat(value, 1/4)) return "1/4"
    if (compareRecipeFloat(value, 3/4)) return "3/4"

    if (compareRecipeFloat(value, 1/5)) return "1/5"
    if (compareRecipeFloat(value, 2/5)) return "2/5"
    if (compareRecipeFloat(value, 3/5)) return "3/5"
    if (compareRecipeFloat(value, 4/5)) return "4/5"

    if (compareRecipeFloat(value, 1/6)) return "1/6"
    if (compareRecipeFloat(value, 5/6)) return "5/6"

    if (compareRecipeFloat(value, 1/7)) return "1/7"
    if (compareRecipeFloat(value, 2/7)) return "2/7"
    if (compareRecipeFloat(value, 3/7)) return "3/7"
    if (compareRecipeFloat(value, 4/7)) return "4/7"
    if (compareRecipeFloat(value, 5/7)) return "5/7"
    if (compareRecipeFloat(value, 6/7)) return "6/7"

    if (compareRecipeFloat(value, 1/8)) return "1/8"
    if (compareRecipeFloat(value, 3/8)) return "3/8"
    if (compareRecipeFloat(value, 5/8)) return "5/8"
    if (compareRecipeFloat(value, 7/8)) return "7/8"

    if (compareRecipeFloat(value, 1/9)) return "1/9"
    if (compareRecipeFloat(value, 2/9)) return "2/9"
    if (compareRecipeFloat(value, 4/9)) return "4/9"
    if (compareRecipeFloat(value, 5/9)) return "5/9"
    if (compareRecipeFloat(value, 7/9)) return "7/9"
    if (compareRecipeFloat(value, 8/9)) return "8/9"

    if (compareRecipeFloat(value, 1/10)) return "1/10"
    if (compareRecipeFloat(value, 3/10)) return "3/10"
    if (compareRecipeFloat(value, 7/10)) return "7/10"
    if (compareRecipeFloat(value, 9/10)) return "9/10"

    // round up to 2 decimapl places
    return `${Number.parseFloat(value.toFixed(2))}`
  }
