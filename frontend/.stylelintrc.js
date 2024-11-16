module.exports = {
  extends: 'stylelint-config-standard-scss',
  plugins: ['stylelint-order'],
  rules: {
    'order/properties-alphabetical-order': true,
    'no-descending-specificity': null,
    'color-function-notation': null,
    'no-empty-source': null,

    // Use kebab-case, expect for any Glue or marketo classes
    'selector-class-pattern':
      '([a-z][a-z0-9]*)(-[a-z0-9]+)*$|(glue).*|(mkto).*|(expansion-panel).*',
  },
  overrides: [
    {
      files: ['**/*.scss'],
      customSyntax: 'postcss-scss',
    },
  ],
};
