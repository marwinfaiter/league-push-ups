<template>
    <div v-for="progress in this.progresses" :key="progress.Username" class="container">
      <table role="button" class="table table-sm table-hover rounded" style="overflow: hidden">
        <thead class="table-light">
          <tr>
            <th>Username</th>
            <th>Kills</th>
            <th>Deaths</th>
            <th>Assists</th>
            <th>Push Ups</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ progress.Username }}</td>
            <td class="text-success">{{ progress.Kills }}</td>
            <td class="text-danger">{{ progress.Deaths }}</td>
            <td class="text-warning">{{ progress.Assists }}</td>
            <td class="text-info">{{ progress.PushUps }}</td>
          </tr>
          <tr>
            <td colspan="5">TEST</td>
          </tr>
        </tbody>
      </table>
    </div>
</template>

<script>

export default {
    name: 'ProgressView',
    data() {
        return {
            progresses: []
        };
    },
    async created() {
        await this.getData();
    },
    methods: {
        async getData() {
            this.progresses = await this.backend_client
              .post("progress")
              .then(response => response.data);
        },
        format_number(number) {
          return parseFloat(number).toFixed(2)
        }
    },
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
