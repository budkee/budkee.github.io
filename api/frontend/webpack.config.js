'use strict'
// Common JS
// const path = require('path');
// const HtmlWebpackPlugin = require('html-webpack-plugin');
// module.exports = {}

// ES6; type: module && export default
import path from 'path';
import * as sass from 'sass';
import { fileURLToPath } from 'url';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';


const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


export default {
    entry: './src/assets/js/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist/public')
    },
    mode: 'development',
    devServer: {
        static: {
            directory: path.join(__dirname, 'dist/public'),
          },
        compress: true,
        port: 8080
    },
    module: {
        rules: [
            {
                test: /\.js$/,  // Para arquivos .js
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.s?[ac]ss$/,  // Para arquivos CSS e SCSS
                use: [
                    {
                    loader: MiniCssExtractPlugin.loader
                    },
                    'css-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                            sassOptions: {
                                quietDeps: true
                            },
                            implementation: sass // Garante o uso da versão correta do Sass
                        }
                    },

                ]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'styles.css'
        })
    ]
};
