<template>
    <table class="container table table-striped table-dark table-hover">
      <thead>
        <tr>
          <th>Match ID</th>
          <th>Team Kills</th>
          <th>Stats</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="match in this.matches" :key="match.MatchID">
          <td>{{ match.MatchID }}</td>
          <td>{{ match.TeamKills }}</td>
          <td>
            <HistoryPlayerStats :players="match.players"/>
          </td>
        </tr>
      </tbody>
    </table>
</template>

<script>
import HistoryPlayerStats from './HistoryPlayerStats.vue';

export default {
    name: 'HistoryView',
    data() {
        return {
            matches: []
        };
    },
    async created() {
        await this.getData();
    },
    methods: {
        async getData() {
            this.matches = await this.backend_client
              .get("matches")
              .then(response => response.data);
        },
    },
    components: { HistoryPlayerStats }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
