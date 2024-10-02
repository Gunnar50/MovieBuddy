import path from 'path';

export default {
  entry: './src/ts/index.ts',
  output: {
    filename: 'bundle.min.js',
    path: path.resolve(__dirname, 'src/static/compiled')
  },
  resolve: {
    extensions: ['.ts', '.js']
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/
      }
    ]
  },
  mode: 'development'
};
