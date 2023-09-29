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
      async onSubmit() {
        if (this.store.state.login) {
          await this.backend_client.logout()
          this.username = "";
          this.password = "";
          this.$router.go("/")
        }
        else {
          await this.backend_client.login(this.username, this.password)
        }
      }
    }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
