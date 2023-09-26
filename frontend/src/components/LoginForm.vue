<template>
  <form class="col-md-10" @submit.prevent="onSubmit">
    <div v-if="!this.store.state.login" class="row g-1 justify-content-end">
        <div class="col-md-4">
          <input type="text" v-model="username" placeholder="username" class="form-control" required>
        </div>
        <div class="col-md-4">
          <input type="password" v-model="password" placeholder="password" class="form-control" required>
        </div>
        <div class="col-md-3">
          <button class="btn btn-primary">Sign in</button>
        </div>
    </div>
    <div>
      <button v-if="this.store.state.login" class="btn btn-primary">Sign out</button>
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
            this.store.commit("set_login", null);
            this.username = "";
            this.password = "";
            this.$router.go("/")
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
        else {
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
</style>
