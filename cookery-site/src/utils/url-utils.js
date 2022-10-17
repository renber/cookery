import config from 'src/config'

export default {

    getPublicUrl (relativeUrl) {
        return `${config.publicPath}${relativeUrl}`     
    }
}