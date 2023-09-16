const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    allowedHosts: "all",
    proxy: {
      '/api': {
        target: 'http://backend:5000',
        pathRewrite: {"^/api": ""},
        ws: true
      },
    },
  }
})
