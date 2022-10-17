export default {
    serverURI: process.env.NODE_ENV === 'production' ? '' : 'http://localhost:3333',
    publicPath: process.env.NODE_ENV === 'production' ? '/cookery' : '',
}
  