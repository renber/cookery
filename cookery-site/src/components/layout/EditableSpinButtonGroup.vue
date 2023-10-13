<template>
  <b-input-group size="sm">
    <b-input-group-prepend>
      <b-button class="py-0" size="sm" @click="decrease">
        <b-icon icon="dash" font-scale="1.6" />
      </b-button>
    </b-input-group-prepend>

    <FractionalNumberInput  :id="id" :size="size" :value="value" @valueChanged="valueChange"></FractionalNumberInput>

    <b-input-group-append>
      <b-button class="py-0" size="sm" @click="increase">
        <b-icon icon="plus" font-scale="1.6" />
      </b-button>
      <b-input-group-text> {{ title }} </b-input-group-text>
      <b-button class="py-0" size="sm" @click="help" style="max-width:20px;padding: 0;">
        <b-icon icon="info" font-scale="1" />
      </b-button>
    </b-input-group-append>
  </b-input-group>
</template>

<script>
import { BIcon, BIconDash, BIconPlus } from 'bootstrap-vue'
import FractionalNumberInput from "components/layout/FractionalNumberInput.vue"

const portionSizeStepsInc = [0.1, 0.15, 0.2, 0.25, 1/3, 0.5, 2/3, 0.75, 1, 1.5, 2]
const portionSizeStepsDec = portionSizeStepsInc.toReversed()

export default {
  name: 'EditableSpinButtonGroup',

  components: {
    FractionalNumberInput,
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
    increase() {
      if (this.value <= portionSizeStepsInc[portionSizeStepsInc.length -1 ]) {
        const newValue = portionSizeStepsInc.find(v => v > this.value) ?? (this.value + 1)
        this.valueChange(newValue)
      } else {
        this.valueChange(this.value + 1)
      }
    },

    decrease() {
      const newValue = portionSizeStepsDec.find(v => v < this.value) ?? this.value - 1
      if (newValue > 0) {
          this.valueChange(newValue)
        }
    },

    help() {
      alert("Eingabe mit Brüchen ist möglich (1/2, 3/8, ...)")
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