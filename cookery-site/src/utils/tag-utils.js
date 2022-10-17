import { colorHash } from 'src/utils/color-hash'

export default {

    getTagDisplayText (title) {
        const colonIdx = title.indexOf(':')
        if (colonIdx == -1) {
            return title
        }

        return title.substring(colonIdx+1)      
    },
    getTagColor(title) {
        // tags are formed like [group]:[value]
        // all tags of the same group should have the same color

        const colonIdx = title.indexOf(':')
        if (colonIdx > -1) {
            return colorHash.hex(title.substring(0, colonIdx))
        } else {
            return colorHash.hex(title)
        }
    }
}