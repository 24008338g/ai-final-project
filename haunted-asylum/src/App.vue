<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background-color: #0a0a0a;
  color: #e0e0e0;
  font-family: 'Cormorant Garamond', serif;
}

#app {
  min-height: 100vh;
  background: linear-gradient(rgba(10, 10, 10, 0.9), rgba(30, 10, 30, 0.8)),
              url('/public/placeholder_image.jpg');
  background-size: cover;
  background-attachment: fixed;
}
</style>