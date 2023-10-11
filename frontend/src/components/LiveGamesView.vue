<template>
  <div class="container-fluid">
    <div class="row" v-for="n in Object.keys(this.events).length" :key="n" style="margin-bottom: 10px;">
      <template v-if="(n - 1) % 2 == 0">
        <div class="col"></div>
          <div :class="(n) in Object.keys(this.events) ? 'col-md-5':'col-md-8'">
            <div class="card">
              <div class="card-header">{{ Object.keys(this.events)[n - 1] }}</div>
              <div class="card-body">
                <Line :id="Object.keys(this.events)[n - 1]" :options="this.chart_options" :data="get_chart_data_by_game_id(Object.keys(this.events)[n - 1])"></Line>
              </div>
            </div>
          </div>
          <div class="col-md-5" v-if="(n) in Object.keys(this.events)">
            <div class="card">
              <div class="card-header">{{ Object.keys(this.events)[n] }}</div>
              <div class="card-body">
                <Line :id="Object.keys(this.events)[n]" :options="this.chart_options" :data="get_chart_data_by_game_id(Object.keys(this.events)[n])"></Line>
              </div>
            </div>
          </div>
          <div class="col"></div>
      </template>
    </div>
  </div>
</template>

<script>
import io from "socket.io-client";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

export default {
    name: 'LiveGamesView',
    components: { Line },
    data() {
      return {
        events: {},
        chart_options: {
          responsive: true,
          scales: {
              y: {
                  ticks: {
                      precision: 0
                  }
              }
          }
        },
        colors: [
          "rgba(0,130,0,0.8)",
          "rgba(0,0,130,0.8)",
          "rgba(130,0,0,0.8)",
          "rgba(130,130,0,0.8)",
          "rgba(0,130,130,0.8)",
        ]
      };
    },
    async created() {
      this.socket = io(process.env.VUE_APP_BACKEND_URL)
      this.socket.on("connect", this.on_connect);
      this.socket.on("live_games", this.on_live_games);
      this.socket.on("disconnect", this.on_disconnect);
      this.socket.on("events", this.on_events);
      this.socket.on("leave", this.on_leave);
      this.socket.emit("join", "frontend");
      this.socket.emit("get_live_games");
    },
    methods: {
      on_connect() {
        console.log("Connected to backend websocket")
      },
      on_disconnect() {
        console.log("Disconnected from backend websocket")
      },
      on_leave(data) {
        delete this.events[data]
      },
      on_events(data) {
        this.events[data["match_id"]] ||= {};
        this.events[data["match_id"]][data["event_time"]] = data["match_players"];
      },
      get_chart_data_by_game_id(game_id) {
        let players = {}

        for (let event_time of Object.keys(this.events[game_id]).sort((a, b) => a-b)) {
          for (let player of this.events[game_id][event_time]) {
            players[player.SummonerName] ||= {};
            players[player.SummonerName]["push_ups"] ||= [];
            players[player.SummonerName]["push_ups"].push(player.push_ups);
            players[player.SummonerName]["kills"] = player.Kills;
            players[player.SummonerName]["deaths"] = player.Deaths;
            players[player.SummonerName]["assists"] = player.Assists;
            players[player.SummonerName]["kda"] = this.format_number(player.kda);
            players[player.SummonerName]["kill_participation"] = this.format_number(player.kill_participation);
          }
        }

        return {
          labels: Object.keys(this.events[game_id]).sort((a, b) => a-b).map((event_time) => new Date(event_time * 1000).toISOString().substring(11,19)),
          datasets: Object.keys(players).sort().map((summoner_name, index) => {
            return {
              data: players[summoner_name]["push_ups"],
              borderColor: this.colors[index],
              tension: 0.3,
              label: `${summoner_name} (${players[summoner_name]["kills"]}/${players[summoner_name]["deaths"]}/${players[summoner_name]["assists"]}) (${players[summoner_name]["kda"]}/${players[summoner_name]["kill_participation"] * 100}%)`
            }
          }),
        }
      },
      format_number(number) {
        return parseFloat(number).toFixed(2);
      },
    }

}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
