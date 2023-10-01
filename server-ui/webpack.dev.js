const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const path = require("path");

module.exports = merge(common, {
	mode: "development",
	output: {
		path: path.resolve(__dirname, "public"),
		filename: "main.js"
	},
	devServer: {
		port: "3000",
		static: ["./public"],
		open: true,
		hot: true ,
		liveReload: true
	},
});
