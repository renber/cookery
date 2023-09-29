<template>
  <b-input-group size="sm">
    <b-input-group-prepend>
      <b-button class="py-0" size="sm" @click="decrease">
        <b-icon icon="dash" font-scale="1.6" />
      </b-button>
    </b-input-group-prepend>

    <b-form-text v-if="!this.editmode" class="border-secondary form-control form-control-md" style="background: white; padding: 4px 10px 0px 10px; margin: 0; cursor: text;" @click="edit(true)">
      {{ formatPortionSize(value)  }}
    </b-form-text>

    <b-form-input
      v-else
      ref="input"
      :id="id"
      :size="size"
      :value="value"
      type="number"
      number
      min="0"
      class="border-secondary text-center"
      @update="valueChange"
      @blur="edit(false)"
    />

    <b-input-group-append>
      <b-button class="py-0" size="sm" @click="increase">
        <b-icon icon="plus" font-scale="1.6" />
      </b-button>
      <b-input-group-text> {{ title }} </b-input-group-text>
    </b-input-group-append>
  </b-input-group>
</template>

<script>
import { BIcon, BIconDash, BIconPlus } from 'bootstrap-vue'
import { formatCommonFractions } from 'src/utils/number-utils.js'

const portionSizeStepsInc = [0.1, 0.15, 0.2, 0.25, 0.33, 0.5, 0.66, 0.75, 1, 1.5, 2]
const portionSizeStepsDec = portionSizeStepsInc.toReversed()

export default {
  name: 'EditableSpinButtonGroup',

  components: {
    BIcon,

    /* eslint-disable vue/no-unused-components */
    BIconDash,
    BIconPlus
  },
  data: () => {
    return {
      editmode: false
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
      required: true
    },

    title: {
      type: String,
      required: true
    }
  },

  methods: {
    valueChange (newValue) {
      if (newValue <= 0) {
        this.$emit('input', 0)
      } else {
        this.$emit('input', newValue)
      }
    },
    edit(enabled) {
      this.editmode = enabled

      if (enabled) {
        this.$nextTick(() => {
          this.$refs.input.select()
        })
      }
    },
    formatPortionSize(value) {
      return formatCommonFractions(value)
    },
    increase() {
      if (this.value <= portionSizeStepsInc[portionSizeStepsInc.length -1 ]) {
        const newValue = portionSizeStepsInc.find(v => v > this.value) ?? (this.value + 1)
        this.valueChange(newValue)
      } else {
        this.valueChange(this.value + 1)
      }
    },

    decrease() {
      if (this.value <= portionSizeStepsDec[0]) {
        const newValue = portionSizeStepsDec.find(v => v < this.value) ?? (this.value - 1)
        this.valueChange(newValue)
      } else {
        this.valueChange(this.value - 1)
      }
    }
  }
}
</script>

<style scoped>
/* Remove up and down arrows inside number input */
/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  appearance: textfield;
}
</style>