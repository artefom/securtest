/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

const myTheme = {
  dark: false,
  colors: {
    background: '#6D5D8F',
    primary: '#FCBE56',
    secondary: '#F27779',
    'on-background': '#ffffff',
  },
}

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'myTheme',
    themes: {
      myTheme,
    }
  },
})
