<!--

Defines the QuickActionBar which is vertical on large views and switches
to horizontal on small ones

Usage:
<QuickActionBar>
     <b-button> <b-icon-file-earmark-plus /> </b-button>
     <b-button> <b-icon-share /> </b-button>
     ...
</QuickActionBar>

-->

<template>
    <div>
        <b-button-group vertical class="d-none d-md-none d-lg-block d-xl-block">
            <ActionButton class="mb-1" v-for="a in actions" :key="a.id" :variant="a.variant" :title="a.title" :icon="a.icon" :hidden="a.hidden" :to="a.to" @click="clicked(a.id)" />
        </b-button-group>
        <b-button-group class="d-xs-block d-sm-block d-md-block d-lg-none d-xl-none">
            <b-button class="mr-1" v-for="a in actions" :key="a.id" :variant="a.variant" :hidden="a.hidden" :to="a.to" @click="clicked(a.id)"> <b-icon :icon="a.icon" /> {{ a.title }} </b-button>
        </b-button-group>
    </div>
</template>

<script>
import ActionButton from 'components/layout/ActionButton'

export default {
    name: 'QuickActionBar',
    components: {
      ActionButton          
    },
    props: {
        'actions': Array
    },
    methods: {
        clicked (actionId) {            
            this.$emit("actionExecuted", actionId)
        }
    }
}
</script>

<style>

#quickactionbar {    
    background: white;    
}

.btn {
    text-decoration: none;
}

</style>