<template>
     <b-button v-if="!hidden" :variant="variant" :to="to" v-b-tooltip.hover.right :title="title" @click="clicked"> <b-icon :icon="icon" /> </b-button>
</template>

<script>
export default {
     name: 'ActionButton',
     props: {
         to: Object,
         icon: String,
         title: String,
         variant: String,
         hidden: {
              type: Boolean,
              default: false
         }
     },
     methods: {
          clicked () {
               this.$emit("click")
          }
     }
}
</script>