<template>
  <NavBar></NavBar>
  <router-view/>
</template>

<script>
  import NavBar from "./components/NavBar.vue";
  import HistoryView from "./components/HistoryView.vue";
  import ProgressView from "./components/ProgressView.vue";
  import APIKeys from "./components/APIKeys.vue";
  import SummonersView from "./components/SummonersView.vue";

  export default {
    name: "App",
    data() {
        return {
            routes: [
              {
                name: "History",
                path: "/history",
                component: HistoryView
              },
              {
                name: "Progress",
                path: "/Progress",
                component: ProgressView
              },
              {
                name: "API Keys",
                path: "/user/api_keys",
                component: APIKeys,
                meta: {
                  requiresAuth: true
                }
              },
              {
                name: "Summoners",
                path: "/user/summoners",
                component: SummonersView,
                meta: {
                  requiresAuth: true
                }
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
