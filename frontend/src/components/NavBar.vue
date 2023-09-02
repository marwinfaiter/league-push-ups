<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="/">League Push Ups</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <div class="navbar-nav mx-auto">
        <router-link to="/live_games" class="nav-link">Live Games</router-link>
        <router-link to="/history" class="nav-link">History</router-link>
        <router-link to="/progress" class="nav-link">Progress</router-link>
      </div>
    </div>
    <div class="navbar-nav me-auto">
      <div v-if="this.store.state.logged_in" class="dropdown">
        <button class="btn btn-success dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <font-awesome-icon :icon="['fas', 'user']" />
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
          <router-link to="/user/api_keys" class="nav-link">API Keys</router-link>
          <router-link to="/user/summoners" class="nav-link">Summoners</router-link>
        </div>
      </div>
      <LoginForm/>
    </div>
  </nav>
</template>

<script>
import LoginForm from './LoginForm.vue';

export default {
  name: 'NavBar',
  components: {
    LoginForm
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.navbar {
  width: 100%;
  padding-left: 10px;
  padding-right: 30px;
  text-align: center;
}

.navbar a {
  font-weight: bold;
  color: #d0d0d0;
}

.navbar a.router-link-exact-active {
  color: whitesmoke;
  background: crimson;
  border-radius: .5rem;
}
</style>
