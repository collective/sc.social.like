var ExtractTextPlugin = require('extract-text-webpack-plugin');
module.exports = {
  entry: './app/index.js',
  output: {
    filename: 'bundle.js',
    path: './dist'
  },
  module: {
    rules: [{
      test: /\.css$/,
      exclude: /node_modules/,
      loader: ExtractTextPlugin.extract({
        loader: 'css-loader?sourceMap'
      })
    }, {
      test: /\.svg/,
      exclude: /node_modules/,
      loader: 'svg-url-loader'
    }]
  },
  devtool: 'source-map',
  plugins: [
    new ExtractTextPlugin({ filename: 'bundle.css', disable: false, allChunks: true })
  ]
}
