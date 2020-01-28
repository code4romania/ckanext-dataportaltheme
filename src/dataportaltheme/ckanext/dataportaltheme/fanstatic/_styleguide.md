# Data Portal CSS/HTML Style Guide

Hi! Thank you for contributing to Data Portal. Please read this before starting to work. Happy styling!

## General

We want **Data Portal** to be accessible to anyone and everyone. 

When writing CSS or HTML, please:
- make browser compatibility and responsiveness one of your top priorities.
- Optimize for screen readers (for hearing impaired users)
- Mind the contrasts (for visually impaired users)


## Formatting

- use 2 spaces for indentation (soft tabs)
- classes should be named using dashes `.class-name`
- functional classes (js hooks) should be prefixed with `.js-` (don't use styling classes or elements as js hooks)
- IDs should be named using camelCase `#customName` (but ID usage should be reduced at a minimum)
-  avoid unnecessary specificity (CSS rules should be as simple as possible)
- avoid using `!important`
- declare all CSS rules in `.css` files, rather than inline or in `<style>` tags in html files
- the opening `{` should be on the same row as the last selector, separated by a space 
- the closing `}` should be on a new line, at the end of the rule declarations
- the `:` should be followed by a space, but not preceded by one.
- comments should pe placed on their own line, avoid end-of-line comments.

 ### 👍 Good:
```
/* Comment on separate line. */
.class-name {
  color: black;
} 
```
 ### 👎 Bad: 
```
.class-name{color:black;} 
.large-header {
  color: red; /*My favorite colour */
  font-size: 36px;
}
```

## Files

- The CSS files are located here: `ckanext/dataportaltheme/fanstatic`
- The main CSS file is `dataportaltheme.css`, where all the theme related global styles should be placed (i.e. general styling of the headings, buttons etc.)
- CSS files are included using the following syntax, on the pages where they are needed: `{% resource  'dataportaltheme/footer.css' %}`
- If a section of the website has specific styling, extract styles in separate CSS file (i.e. `footer.css`, `header.css`, `sidebar.css` etc.)

