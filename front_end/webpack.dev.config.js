const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { HotModuleReplacementPlugin } = require('webpack');

module.exports = {
  target: 'web',
  mode: 'development',
  entry: [
    'core-js/modules/es.promise',
    'core-js/modules/es.array.iterator',
    './src/index.js'
  ],
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.m?js$/i,
        exclude: (file) => /node_modules/.test(file) && !/\.vue\.js/.test(file),
        use: {
          loader: 'babel-loader'
        }
      },
      {
        test: /\.vue$/i,
        use: {
          loader: 'vue-loader'
        }
      },
      {
        test: /\.(css|scss)$/i,
        use: ['style-loader', 'css-loader', 'sass-loader']
      },
      {
        test: /\.less$/i,
        use: [
          'style-loader',
          'css-loader',
          {
            loader: 'less-loader',
            options: {
              lessOptions: {
                javascriptEnabled: true
              }
            }
          }
        ]
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        use: {
          loader: 'file-loader'
        }
      }
    ]
  },
  plugins: [
    new VueLoaderPlugin(),
    new CleanWebpackPlugin({
      cleanOnceBeforeBuildPatterns: ['**/*']
    }),
    new HtmlWebpackPlugin({
      template: path.join(__dirname, 'public', 'index.html'),
      inject: 'body'
    }),
    new HotModuleReplacementPlugin()
  ],
  resolve: {
    alias: {
      vue$: 'vue/dist/vue.esm-bundler.js'
    }
  },
  devtool: 'eval-cheap-source-map',
  devServer: {
    port: 9000,
    contentBase: path.resolve(__dirname, 'dist'),
    compress: true,
    // historyApiFallback: {
    //   rewrites: [
    //     {
    //       from: /^\/seller\/.*$/,
    //       to: '/seller'
    //     }
    //   ]
    // },
    stats: 'minimal',
    inline: true,
    open: true,
    hot: true
  }
};
