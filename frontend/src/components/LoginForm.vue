<template>
  <form @submit.prevent="onSubmit">
    <div class="row">
      <template v-if="!this.store.state.login">
        <!-- User input -->
        <div class="col">
          <input type="text" v-model="username" placeholder="username" class="form-control" />
        </div>

        <!-- Password input -->
        <div class="col">
          <input type="password" v-model="password" placeholder="password" class="form-control" />
        </div>
      </template>

      <!-- Submit button -->
      <button v-if="this.store.state.login" class="btn btn-primary col">Sign out</button>
      <button v-else class="btn btn-primary col">Sign in</button>
    </div>
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
      onSubmit() {
        if (this.store.state.login) {
          this.backend_client.logout()
          .then(response => {
            this.store.commit("set_login", null)
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
        else if(this.username && this.password) {
          this.backend_client.login(this.username, this.password)
          .then(response => {
            if (response) {
              this.store.commit("set_login", response.data);
              return response;
            }
          })
          .catch(error => {
            this.store.commit("set_login", false)
            if (error.response) {
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            }
          })
        }
      }
    }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
form {
  margin-left: 20px;
}
</style>
