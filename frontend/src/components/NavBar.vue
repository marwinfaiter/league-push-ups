<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <router-link to="/" class="navbar-brand" style="background: none;"><img style="width: 40px; border-radius: 100px; margin: 0px" src="~@/assets/LPU.png"></router-link>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <div class="navbar-nav">
        <router-link to="/live_games" class="nav-link">Live Games</router-link>
        <router-link to="/history" class="nav-link">History</router-link>
        <router-link to="/progress" class="nav-link">Progress</router-link>
      </div>
    </div>
    <div class="navbar-nav me-auto">
      <div class="container">
        <div class="row justify-content-end">
          <div v-if="this.store.state.login" class="dropdown col-md-2">
            <button class="btn btn-success dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <font-awesome-icon :icon="['fas', 'user']" />
            </button>
            <div class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton">
              <router-link to="/user/settings" class="nav-link">Settings</router-link>
              <router-link v-if="this.store.state.login.groups.includes('leaguepushups-admins')" to="/rewards" class="nav-link">Rewards</router-link>
            </div>
          </div>
          <LoginForm/>
        </div>
      </div>
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
