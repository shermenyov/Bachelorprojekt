module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: ['plugin:vue/vue3-essential', 'eslint:recommended', 'plugin:prettier/recommended'],
  parserOptions: {
    parser: '@babel/eslint-parser',
  },
  rules: {
    'max-len': [
      'warn',
      {
        code: 120,
      },
    ],
    semi: ['error', 'never'],
    quotes: ['warn', 'single'],
  },
}
