const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  // Output to Flask static folder
  outputDir: "dist",
  // Configure dev server for local development
  devServer: {
    port: 8080,
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
        pathRewrite: {
          "^/api": ""
        }
      },
    },
  },
  // Disable eslint on build
  lintOnSave: false
});
