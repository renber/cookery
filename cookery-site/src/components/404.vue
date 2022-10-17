<template>
    <ContentLayout>
        <template v-slot:sidebar>
             <h3>
                Was nun?
            </h3>
        </template>

        <template v-slot:content>
          <b-container>
            <b-row align-h="center">
              <img :src="require('@/assets/img/404.png')" />
            </b-row>
            <b-row align-h="center">
              Die gesuchte Seite existiert nicht.
            </b-row>
          </b-container>            
        </template>

        <template v-slot:actions>
            <b-button> <b-icon-back /> </b-button>            
        </template>
    </ContentLayout>
</template>

<script>
import ContentLayout from 'components/layout/ContentLayout'

export default {
  name: 'NotFound',

  components: {
      ContentLayout      
  }
}
</script>