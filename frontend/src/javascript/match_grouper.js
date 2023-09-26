export default class MatchGrouper {
    constructor(identifier, matches) {
        this.identifier = identifier;
        this.matches = matches;
    }
    static group_by_year(matches) {
        return Object.values(matches.reduce((match_groupers, match) => {
            let date_match = match.MatchDateTime.match(/^(\d{4})/);
            match_groupers[date_match[1]] ||= new MatchGrouper(date_match[1], []);
            match_groupers[date_match[1]].matches.push(match);
            return match_groupers;
        }, {}));
    }
    static group_by_month(matches) {
        return Object.values(matches.reduce((match_groupers, match) => {
            let date_match = match.MatchDateTime.match(/^(\d{4}-\d{2})/);
            match_groupers[date_match[1]] ||= new MatchGrouper(date_match[1], []);
            match_groupers[date_match[1]].matches.push(match);
            return match_groupers;
        }, {}));
    }
    static group_by_day(matches) {
        return Object.values(matches.reduce((match_groupers, match) => {
            let date_match = match.MatchDateTime.match(/^(\d{4}-\d{2}-\d{2})/);
            match_groupers[date_match[1]] ||= new MatchGrouper(date_match[1], []);
            match_groupers[date_match[1]].matches.push(match);
            return match_groupers;
        }, {}));
    }
    static group_by_match(matches) {
        return matches.map(match => new MatchGrouper(match.MatchID, [match]))
    }
    static group_by_session(matches) {
        return Object.values(matches.reduce((match_groupers, match) => {
            match_groupers[match.SessionID] ||= new MatchGrouper(match.SessionID, []);
            match_groupers[match.SessionID].matches.push(match);
            return match_groupers;
        }, {}));
    }
    get kills() {
        return this.matches.map(match => match.Kills).reduce((a, b) => a + b);
    }
    get avg_kills() {
        return this.kills / this.matches.length;
    }
    get deaths() {
        return this.matches.map(match => match.Deaths).reduce((a, b) => a + b);
    }
    get avg_deaths() {
        return this.deaths / this.matches.length;
    }
    get assists() {
        return this.matches.map(match => match.Assists).reduce((a, b) => a + b);
    }
    get avg_assists() {
        return this.assists / this.matches.length;
    }
    get avg_kda() {
        return this.matches.map(match => match.KDA).reduce((a, b) => a + b) / this.matches.length
    }
    get avg_kill_participation() {
        return this.matches.map(match => match.KillParticipation).reduce((a, b) => a + b) / this.matches.length
    }
    get push_ups() {
        return this.matches.map(match => {return match.Active ? match.PushUps : 0}).reduce((a, b) => a + b);
    }
    get avg_push_ups() {
        return this.push_ups / this.matches.length;
    }
}
