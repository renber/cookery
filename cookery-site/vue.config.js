var path = require('path')
module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/cookery/' : '/',
  configureWebpack: {
    resolve: {
      alias: {
        src: path.resolve(__dirname, 'src'),
        components: path.resolve(__dirname, 'src/components')
      }
    },
  }
}