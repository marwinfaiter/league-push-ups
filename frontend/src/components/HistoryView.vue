<template>
    <div v-for="match in this.matches" :key="match.id" class="container">
      <table role="button" data-bs-toggle="modal" data-bs-target="#match_modal" class="table table-sm table-hover rounded" style="overflow: hidden">
        <thead class="table-light">
          <tr>
            <th>SummonerName</th>
            <th>Kills</th>
            <th>Deaths</th>
            <th>Assists</th>
            <th>KDA</th>
            <th>Kill Participation</th>
            <th>Push Ups</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="player in match.players" :key="player.id">
            <td>{{ player.SummonerName }}</td>
            <td class="text-success">{{ player.Kills }}</td>
            <td class="text-danger">{{ player.Deaths }}</td>
            <td class="text-warning">{{ player.Assists }}</td>
            <td>{{ format_number(player.KDA) }}</td>
            <td>{{ format_number(player.KillParticipation * 100) }}%</td>
            <td class="text-info">{{ player.PushUps }}</td>
          </tr>
        </tbody>
      </table>
      <div class="modal" id="match_modal">
        <div class="modal-dialog">
          <div class="modal-content">
            <table class="table table-borderless table-sm table-hover rounded" style="overflow: hidden; margin: 0">
              <thead class="table-light">
                <tr>
                  <th>Game ID</th>
                  <th>Team Kills</th>
                  <th>Minimum Push Ups</th>
                  <th>Maximum Push Ups</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{{ match.MatchID }}</td>
                  <td>{{ match.TeamKills }}</td>
                  <td>{{ match.MinPushUps }}</td>
                  <td>{{ match.MaxPushUps }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

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
              .then(response => response.data.reverse());
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
