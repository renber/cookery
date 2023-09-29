
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

export function formatCommonFractions(value) {

    if (!value) {
      return "";
    }
    if (value === 0.75) {
      return "3/4" // ¾
    }
    if (value == 2/3 || value === 0.66) {
      return "2/3" // ⅔
    }
    if (value === 0.5) {
      return "1/2" // ½
    }
    if (value === 1/3 || value === 0.33) {
      return "1/3" // ⅓
    }
    if (value === 0.25) {
      return "1/4" // ¼
    }
    if (value === 0.2) {
      return "1/5" // ⅕
    }
    if (value === 0.15) {
      return "1/8" // ⅛
    }
    if (value === 0.1) {
      return "1/10" // ⅒
    }

    // round up to 2 decimapl places
    return Math.ceil( value * 100 + Number.EPSILON ) / 100
  }