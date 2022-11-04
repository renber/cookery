<!--

    Image and Textoverlay for previews

-->

<template>
    <router-link :to="{ name: recipe.group+'-recipe-details', params: {id: recipe.short_id, readableId: recipe.readable_id } }" class="recipe-card">
      <b-card class="h-100 text-center" no-body bg-variant="primary" text-variant="white">
          <img v-if="recipe.image_url" class="card-img card-img-top img-fluid" :src="recipe.image_url" :style="`height:${imgHeight}`" top />
          <img v-else class="card-img card-img-top img-fluid no-img-placeholder" :style="`height:${imgHeight}`" top />

          <!-- put tags on top of image -->
          <tag-view v-if="withTags && recipe.tags && recipe.tags.length > 0" :tags="recipe.tags" class="tag-overlay" />

          <template #footer>
            {{ recipe.title }}
          </template>
      </b-card>

    </router-link>
</template>

<script>
import TagView from 'components/layout/TagView.vue'

export default {
  name: 'PreviewTile',
  components: {
    TagView
  },
  props: {
    recipe: Object,
    withTags: {
      type: Boolean,
      default: false
    },
    imgHeight: {
      type: String,
      default: "200px"
    }
  }
}
</script>

<style scoped>
  .card-img {
      width: 100%;
      object-fit: cover;
  }

  .no-img-placeholder {
    content: url('assets/img/no_image_placeholder_blurred.jpg');
  }

  a.recipe-card,
    a.recipe-card:hover {
        color: inherit;
        text-decoration: none;
    }

  .tag-overlay {
    text-align:start;
    position: absolute;
    top: 110px; max-height:
    40px; overflow: hidden;
    margin-left: 5px;
    margin-right: 5px
  }
</style>