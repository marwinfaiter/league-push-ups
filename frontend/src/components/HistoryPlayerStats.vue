<template>
  <table class="container table table-striped table-dark table-hover">
    <thead>
      <tr>
        <th>SummonerName</th>
        <th>Kills</th>
        <th>Deaths</th>
        <th>Assists</th>
        <th>KDA</th>
        <th>Kill Participation</th>
        <th>PushUps</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="player in this.players" :key="player.id">
        <td>{{ player.SummonerName }}</td>
        <td>{{ player.Kills }}</td>
        <td>{{ player.Deaths }}</td>
        <td>{{ player.Assists }}</td>
        <td>{{ player.KDA }}</td>
        <td>{{ player.KillParticipation * 100}}%</td>
        <td>{{ player.PushUps }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'HistoryPlayerStats',
  props: {
    players: Array
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
