/** @type {import('tailwindcss').Config} */
module.exports = {
  content:["./src/**/*.{html,svelte,js,ts}"],
  darkMode: 'class',
  theme: {
    extend:{
      screens: {
        sm: '480px',
        md: '768px',
        lg: '976px',
        xl: '1440px',
      },
      colors: {
        "error": "#F53B3B",
        "white":{"50":"#FCFCFC","100":"#FCFCFC","200":"#FAFAFA","300":"#F7F7F7","400":"#F5F5F5","500":"#F1F1F1","600":"#C2C2C2","700":"#919191","800":"#616161","900":"#303030","950":"#171717"},
        "primary":{"50":"#E5FFF4","100":"#CCFFEA","200":"#99FFD5","300":"#66FFBF","400":"#33FFAA","500":"#00FF95","600":"#00CC77","700":"#009959","800":"#00663C","900":"#00331E","950":"#00190F"},
        "secondary":{"50":"#F5E5FF","100":"#EBCCFF","200":"#D699FF","300":"#C266FF","400":"#AD33FF","500":"#9800FF","600":"#7A00CC","700":"#5C0099","800":"#3D0066","900":"#1F0033","950":"#0F0019"},
        "background": "#202731",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}

