<template>
  <div class="container">
    <div v-for="game_id in Object.keys(this.events)" :key="game_id" class="card">
      <div class="card-header">{{ game_id }}</div>
      <div class="card-body">
        <Line :id="game_id" :options="get_chart_options()" :data="get_chart_data_by_game_id(game_id)"></Line>
      </div>
    </div>
  </div>
  </template>

<script>
import io from "socket.io-client";

import {
  Chart as ChartJS,
  Colors,
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
  Colors,
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
        events: {}
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

        for (let event_time of Object.keys(this.events[game_id]).sort()) {
          for (let player of this.events[game_id][event_time]) {
            players[player.SummonerName] ||= {};
            players[player.SummonerName]["push_ups"] ||= [];
            players[player.SummonerName]["push_ups"].push(player.push_ups);
            players[player.SummonerName]["kills"] = player.Kills;
            players[player.SummonerName]["deaths"] = player.Deaths;
            players[player.SummonerName]["assists"] = player.Assists;
            players[player.SummonerName]["kda"] = player.kda;
            players[player.SummonerName]["kill_participation"] = player.kill_participation;
          }
        }

        return {
          labels: Object.keys(this.events[game_id]).sort().map((event_time) => new Date(event_time * 1000).toISOString().substring(11,19)),
          datasets: Object.keys(players).sort().map((summoner_name) => {
            return {
              data: players[summoner_name]["push_ups"],
              label: `${summoner_name} (${players[summoner_name]["kills"]}/${players[summoner_name]["deaths"]}/${players[summoner_name]["assists"]}) (${players[summoner_name]["kda"]}/${players[summoner_name]["kill_participation"] * 100}%)`
            }
          })
        }
      },
      get_chart_options() {
        return {
          responsive: true,
          scales: {
              y: {
                  ticks: {
                      precision: 0
                  }
              }
          }
        }
      }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
