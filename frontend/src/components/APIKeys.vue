<template>
  <div class="container">
    <table class="table table-sm table-hover rounded" style="overflow: hidden">
      <thead class="table-light">
        <tr>
          <th>API Keys</th>
          <th><button @click="create_api_key" class="btn btn-primary">Create</button></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="api_key in this.api_keys" :key="api_key.id">
          <td>{{ api_key.value }}</td>
          <td><button type="button" @click="delete_api_key(api_key.value)" class="btn btn-danger">Delete</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
    name: 'APIKeys',
    data() {
      return {
        api_keys: []
      };
    },
    async created() {
      await this.getData();
    },
    methods: {
      async getData() {
        this.api_keys = await this.backend_client
          .get("api_keys")
          .then(response => response.data);
      },
      async create_api_key() {
        await this.backend_client.post("api_keys");
        this.$router.go()
      },
      async delete_api_key(api_key) {
        await this.backend_client.delete("api_keys", api_key)
        this.$router.go()
      }
    },
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
