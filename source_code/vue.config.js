module.exports = {
  // publicPath: '/cloud_schedule/',
  productionSourceMap: false,
  chainWebpack: config => {
    config.plugins.delete('prefetch')
    config
      .plugin('html')
      .tap(args => {
        args[0].title= '云日程'
        return args
      })
  }
}
