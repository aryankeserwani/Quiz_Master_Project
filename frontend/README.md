# Quiz Master Frontend

This is the frontend application for Quiz Master, built with Vue 3 and Vue CLI.

## Project Setup

```bash
# Install dependencies
npm install
```

### Development Server

```bash
# Start the development server
npm run serve
```

### Production Build

```bash
# Compile and minify for production
npm run build
```

### Linting

```bash
# Lint the project
npm run lint
```

## Migration from Vue 2 to Vue 3

This project has been migrated from Vue 2 to Vue 3. The key changes include:

1. Upgraded from Vue 2.6 to Vue 3.3
2. Migrated from Vue Router 3 to Vue Router 4
3. Converted all components from Options API to Composition API
4. Replaced global Vue properties with composables
5. Improved code organization with composables for shared functionality

## Application Structure

- `src/components/` - Vue components
- `src/composables/` - Reusable composition functions (Vue 3)
- `src/router/` - Vue Router configuration
- `src/assets/` - Static assets like images and styles

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).
