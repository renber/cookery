<template>
     <b-form-input
      ref="input"
      :size="size"
      :value="displayValue"
      type="text"
      class="border-secondary text-center"
      @click="selectAll"
      @update="valueChanged"
      @blur="focusLost"
    />
</template>

<script>

import { parseCommonFraction, formatCommonFraction, compareRecipeFloat } from 'src/utils/number-utils'

export default {
  name: 'FractionalNumberInput',

  data: () => {
    return {
        displayValue: '0'
    }
  },
  props: {
    id: {
      type: String,
      required: true
    },

    size: {
      type: String,
      required: false,
      default: 'md',
      validator: function (value) {
        return ['sm', 'md', 'lg'].includes(value)
      }
    },

    value: {
      type: Number,
      required: true,
    }
  },
  watch: {
    value: function(newValue, oldValue) {
      const f = parseCommonFraction(this.displayValue)
      if (!compareRecipeFloat(f, newValue)) {
        this.displayValue = formatCommonFraction(newValue)
      }
    }
  },
  mounted() {
    this.displayValue = formatCommonFraction(this.value)
  },
  methods: {
    selectAll() {
        this.$refs.input.select()
    },

    valueChanged (newValue) {
      const f = parseCommonFraction(newValue)
      this.$nextTick(() => {
      if (Number.isNaN(f)) {
        this.displayValue = newValue
      } else {
        if (f <= 0) {
          this.displayValue = '0'
          this.$emit('valueChanged', 0)
        } else {
          this.displayValue = newValue
          this.$emit('valueChanged', f)
        }
      }
    })
    },
    formatValue() {
        this.displayValue = formatCommonFraction(this.value)
    },
    focusLost() {
      this.$nextTick(() => {
        this.displayValue = formatCommonFraction(this.value)
      })
    }
  }
}

</script>

<style scoped>

</style>