const Dotenv = require('dotenv-webpack');
const webpack = require('webpack');

module.exports = {
  webpack: (config) => {
    // Add the dotenv plugin
    // config.plugins.push(new Dotenv({ path: './frontend.env' }));

    // Add global constants
    config.plugins.push(
      new webpack.DefinePlugin({
        'process.env.REACT_APP_DEVELOPMENT_MODE': JSON.stringify(process.env.REACT_APP_DEVELOPMENT_MODE),
        'process.env.REACT_APP_DOCKERIZED': JSON.stringify(process.env.REACT_APP_DOCKERIZED),
      })
    );

    return config;
  },
};
