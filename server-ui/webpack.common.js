const path = require("path");
const TerserPlugin = require("terser-webpack-plugin");

module.exports={
	entry: path.resolve(__dirname, "src", "index.js"),
	optimization: {
		minimize: true,
		minimizer: [
			new TerserPlugin({
				extractComments: false,
			}),
		],
	},
	target: "web",
	resolve: {
		extensions: ['.js','.jsx','.json'] 
	},
	module:{
		rules: [
			{
				test: /\.(js|jsx)$/,        // kind of file extension this rule should look for and apply in test
				exclude: /node_modules/,    // folder to be excluded
				use:  'babel-loader'        // loader which we are going to use
			}
		]
	},
};
