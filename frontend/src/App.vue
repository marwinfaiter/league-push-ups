<template>
  <NavBar></NavBar>
  <router-view/>
</template>

<script>
  import NavBar from "./components/NavBar.vue";
  import HistoryView from "./components/HistoryView.vue";

  export default {
    name: "App",
    data() {
        return {
            routes: [
              {
                path: "/history",
                component: HistoryView
              }
            ]
        };
    },
    computed: {
        username() {
            // We will see what `params` is shortly
            return this.$route.params.username;
        },
    },
    components: {
      NavBar
    }
}
</script>

<style lang="scss">
  html {
    padding: 0;
    margin: 0;
    width: 100%;
    min-height: 100%; // add this rule
  }
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  body {
    background-image: url('~@/assets/Background.jpg');
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
  }
</style>
