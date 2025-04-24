const path = require("path");
const HTMLPlugin = require("html-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
  entry: {
    index: "./src/index.tsx",
    content: "./src/components/ContentScript.tsx"  // new entry for content script
  },
  mode: "production",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: [
          {
            loader: "ts-loader",
            options: {
              compilerOptions: { noEmit: false },
            }
          }
        ],
        exclude: /node_modules/,
      },
      {
        test: /\.(png|jpe?g|gif)$/i,
        use: [
          {
            loader: "file-loader",
          }
        ],
      },
      {
        exclude: /node_modules/,
        test: /\.css$/i,
        use: [
          "style-loader",
          "css-loader",
          "postcss-loader"
        ]
      }
    ],
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        { from: "public/", to: "images/" },
        { from: "src/background.js", to: "background.js" },
        { from: "src/scrapeScript.js", to: "scrapeScript.js" },
        // Removed: { from: "src/content.js", to: "content.js" },
        { from: "manifest.json", to: "../manifest.json" }
      ],
    }),
    ...getHtmlPlugins(["index"]),
  ],
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
  output: {
    path: path.join(__dirname, "dist/js"),
    filename: "[name].js", // This will produce index.js and content.js in dist/js
  },
};

function getHtmlPlugins(chunks) {
  return chunks.map(chunk =>
    new HTMLPlugin({
      title: "React extension",
      filename: `${chunk}.html`,
      chunks: [chunk],
    })
  );
}
