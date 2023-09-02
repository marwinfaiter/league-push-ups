<template>
  <form v-if="!this.store.state.logged_in">
    <div class="row">
      <!-- User input -->
      <div class="col">
        <input type="text" v-model="username" placeholder="username" class="form-control" />
      </div>

      <!-- Password input -->
      <div class="col">
        <input type="password" v-model="password" placeholder="password" class="form-control" />
      </div>

      <!-- Submit button -->
      <button @click="login" class="btn btn-primary col">Sign in</button>
    </div>
  </form>
  <form v-else>
      <!-- Submit button -->
      <button @click="logout" class="btn btn-primary col">Sign out</button>
  </form>
</template>

<script>
export default {
    name: 'LoginForm',
    data() {
      return {
        username: "",
        password: "",
      }
    },
    methods: {
      login() {
        if (!this.username || !this.password) {
          return
        }
        this.backend_client.login(this.username, this.password)
          .then(response => {
            this.store.commit("set_login", true)
            return response;
          })
          .catch(error => {
            this.store.commit("set_login", false)
            if (error.response) {
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            }
          })
      },
      logout() {
        if (!this.store.state.logged_in) {
          return
        }

        this.backend_client.logout()
          .then(response => {
            this.store.commit("set_login", false)
            return response;
          })
          .catch(error => {
            if (error.response) {
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            }
          })
      }
    }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
form {
  margin-left: 10px;
}
</style>
