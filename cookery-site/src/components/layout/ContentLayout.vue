<!--

The main layout component with left column, large content column and QuickNavigationBar

-->

<template>
    <b-container fluid id="main-container">
        <b-row no-gutters class="align-self-stretch">
            <b-col sm="12" md="4" lg="3" xl="3" id="sidebar">
                <slot name="sidebar" />
            </b-col>
            <b-col  class="pl-xs-0 pl-sm-0 pl-md-2 pl-lg-2 pl-xl-2" >
                <div id="content">
                    <slot name="content" />
                </div>
            </b-col>
            <!-- only reserve space for the action bar if there are actions -->
            <b-col v-if="actions && actions.length > 0" xs="12" sm="12" md="12" lg="1" xl="1">
                <QuickActionBar class="text-right" :actions="actions" @actionExecuted="actionExecuted" />
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import QuickActionBar from 'components/layout/QuickActionBar'

export default {
  name: 'ContentLayout',
  components: {
      QuickActionBar
  },
  props: {
      'actions': Array
  },
  methods: {
        actionExecuted (actionId) {
            this.$emit("actionExecuted", actionId)
        }
    }
}
</script>

<style>
    #main-container {
        padding-left: 0;
        padding-right: 0;
    }

    #content {
        min-height: 500px;
        height: 100%;
    }
</style>