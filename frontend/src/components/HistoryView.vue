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
            <table class="container table table-striped table-dark table-hover">
              <thead>
                <tr>
                  <th>SummonerName</th>
                  <th>Kills</th>
                  <th>Deaths</th>
                  <th>Assists</th>
                  <th>PushUps</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="player in match.players" :key="player.id">
                  <td>{{ player.SummonerName }}</td>
                  <td>{{ player.Kills }}</td>
                  <td>{{ player.Deaths }}</td>
                  <td>{{ player.Assists }}</td>
                  <td>{{ player.PushUps }}</td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
</template>

<script>
export default {
  name: 'HistoryView',
  data() {
    return {
      matches: []
    }
  },
  async created() {
    await this.getData();
    console.log(this.matches);
  },
  methods: {
    async getData() {
      this.matches = await this.backend_client.get("matches");
    },
  },
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
