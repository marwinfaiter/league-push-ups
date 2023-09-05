<template>
  <div class="container">
    <table class="table table-sm table-hover rounded" style="overflow: hidden">
      <thead class="table-light">
        <tr>
          <th>Summoners</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="summoner in this.summoners" :key="summoner.id">
          <td>{{ summoner.name }}</td>
          <td><button type="button" @click="delete_summoner(summoner.name)" class="btn btn-danger">Delete</button></td>
        </tr>
        <tr>
          <td><input v-model="new_summoner" placeholder="New Summoner"></td>
          <td><button @click="add_summoner" class="btn btn-primary">Add</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
    name: 'SummonersView',
    data() {
      return {
        summoners: [],
        new_summoner: "",
      };
    },
    async created() {
      await this.getData();
    },
    methods: {
      async getData() {
        this.summoners = await this.backend_client.get("summoners").then(response => response.data);
      },
      async add_summoner() {
        await this.backend_client.post("summoners", this.new_summoner).then(response => {
            if (response) {
              this.$router.go();
              return response;
            }
        });
      },
      async delete_summoner(summoner) {
        await this.backend_client.delete("summoners", summoner).then(response => {
          if (response) {
              this.$router.go();
              return response;
            }
        })
      }
    },
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
