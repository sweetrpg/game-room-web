
const CreateEncounterDialog = {
    name: 'create-encounter-dialog',
    data: function() {
        return {
            name: '',
            gameSystem: '',
            ordering: '',
            theme: '',
        }
    },
    computed: {
gameSystems: function() {
        return this.$store.state.gameSystems;
}
    },
    methods: {
      },
  beforeMount: function () {
    console.log('Fetching game systems');
    this.$store.dispatch('fetchGameSystems')
  },
    template: `
<div class="modal fade" id="createEncounterDialog" tabindex="-1" role="dialog" aria-labelledby="createEncounterModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="createEncounterModalLabel">Create Encounter</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <form>
        <div class="modal-body">
          <div class="form-group">
            <div class="input-group">
              <div class="input-group-prepend">
                <label class="input-group-text" for="encounterName">Name</label>
              </div>
              <input type="text" class="form-control" id="encounterName" aria-describedby="nameHelp" placeholder="..." autofocus>
              <div class="input-group-append">
                <button id="button-random-name"
                        class="btn btn-outline-secondary input-group-text" type="button"
                        onclick="getRandomName('group')">
                  <img src="/static/images/button-reset.png" alt="Random" />
                </button>
              </div>
            </div>
            <small id="nameHelp" class="form-text text-muted">
            Enter a name for the new encounter.
            </small>
          </div>

          <div class="form-group">
            <div class="input-group">
              <div class="input-group-prepend">
                <label class="input-group-text" for="gameSystem">Ordering</label>
              </div>
              <select class="form-control custom-select" id="ordering" aria-describedby="orderingHelp">
                <option value="high-to-low" selected>High-to-low</option>
                <option value="low-to-high">Low-to-high</option>
                <option value="pc-v-adversary">PC vs Adversary Grouping</option>
                <option value="player-managed">Player-managed</option>
              </select>
            </div>
            <small id="orderingHelp" class="form-text text-muted">
            Ordering determines how the initiative tracker will arrange the participants
            when the encounter is in progress.<br/>
            <b>PC vs Adversary Grouping</b> means that the order is divided between the PCs
            and the adversaries, with objects going last.<br/>
            <b>Player-managed</b> means that there is no order, and the players determine
            who goes when.
            </small>
          </div>

          <div class="form-group">
            <div class="input-group">
              <div class="input-group-prepend">
                <label class="input-group-text" for="gameSystem">Game System</label>
              </div>
              <select class="form-control custom-select" id="gameSystem" aria-describedby="gameSystemHelp">
                <option value="none" selected>None</option>
                <option v-for="gs in gameSystems" v-bind:value="gs.key">{{ gs.name }}</option>
              </select>
            </div>
            <small id="gameSystemHelp" class="form-text text-muted">
            A game system can be selected, which will allow the use of a health tracker
            that understands the rules of the system.
            </small>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary">Create</button>
        </div>
      </form>
    </div>
  </div>
</div>
    `
}
