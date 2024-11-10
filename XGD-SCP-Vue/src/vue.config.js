const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  devServer: {
    proxy: {
      '/api': {
        target: 'https://localhost:8834',
        changeOrigin: true,
        secure: false, // 如果是 HTTPS，需要设置为 false
        pathRewrite: { '^/api': '' } // 重写路径
      }
    }
  }
});