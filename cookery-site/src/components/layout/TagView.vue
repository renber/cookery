<template>    
    <b-form-tags v-model="tags" class="read-only-tag-view" placeholder="" disabled>
            <template v-slot="{tags}">
                    <b-form-tag
                        v-for="tag in tags"        
                        :key="tag"
                        :title="tag"
                        :style="{'font-size': '11pt', 'background-color': getTagColor(tag)}"
                        class="mr-1"  
                        disabled          
                    >{{ getTagDisplayText(tag) }}</b-form-tag>        
            </template> 
    </b-form-tags>
</template>

<script>
import TagUtils from 'src/utils/tag-utils'

export default {
    name: 'TagView',    
    props: {
        tags: Array
    },
    methods: {
        getTagDisplayText (value) {
        // display the tag without its category (part before colon)
        return TagUtils.getTagDisplayText(value)
        },
        getTagColor (value) {            
            return TagUtils.getTagColor(value)
        }
    }
}
</script>

<style scoped>
    .read-only-tag-view {
        background-color: transparent;
        border-radius: 0;
        border: none;
        padding: 0.5em 0 0 0;
    }

    .b-form-tag.disabled {
    /* usually disabled tags get an opacity of 0.75, but we do not want this */  
        opacity: 1;
    }
</style>