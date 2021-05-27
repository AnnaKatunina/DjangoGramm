const path = require('path');
const MiniCssEctractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: './src/js/index.js',
  mode: 'development',
  output: {
    path: path.resolve(__dirname, 'app_DjangoGramm/static/js'),
    filename: 'index.js',
  },
  module: {
    rules: [
        {
          test: /\.(scss)$/,
          use: [MiniCssEctractPlugin.loader, 'css-loader', 'sass-loader']
        }
    ],
  },
  plugins: [
      new MiniCssEctractPlugin({
        filename: '../css/index.css',
      })
  ]
};