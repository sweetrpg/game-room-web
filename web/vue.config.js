const path = require('path');

module.exports = {
    assetsDir: '../assets',
    publicPath: process.env.NODE_ENV === 'production' ? '/shelf/' : '/',
    outputDir: path.resolve(__dirname, '../../src/sweetrpg_shelf_web/templates'),
    runtimeCompiler: undefined,
    productionSourceMap: undefined,
    parallel: undefined,
    css: undefined
};
