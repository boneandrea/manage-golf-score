// import globals from "globals"
import jsdoc from "eslint-plugin-jsdoc"
import pluginVue from 'eslint-plugin-vue'

export default [
  {
    // 1. ルールの対象を glob pattern で指定できるようになりました。
    files: ["**/*.js", "**/*.vue"],
    languageOptions: {
      // 2. env オプションは無くなり、代わりに globals を使用するようになりました。
      globals: {
        // ...globals.browser,
        // ...globals.node
      },
      // eslintrc の parserOptions と同じです。
      parserOptions: {
        ecmaVersion: "latest"
      },
    },
    // 3. plugin は名称を指定できるようになりましたが、注意があります。
    plugins: {
      jsdoc,
    },
    // rule の書き方は基本的に同じです。
    rules: {
      "jsdoc/require-description": "error"
    }
  },
  ...pluginVue.configs['flat/recommended'],
]
