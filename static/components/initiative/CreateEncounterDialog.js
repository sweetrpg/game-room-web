
const CreateEncounterDialog = {
  name: 'create-encounter-dialog',
  data() {
    return {
      name: '',
      gameSystem: 'none',
      ordering: 'high-to-low',
      theme: '',
    }
  },
  computed: {
    gameSystems() {
      return this.$store.state.gameSystems;
    }
  },
  methods: {
    getRandomName() {
      console.log("getRandomName");
      axios.get('/api/v1/random/name?type=group')
        .then((response) => {
          console.log(response);
          console.log(this);
          this.name = response.data.name;
          $('#createEncounterName').val(response.data.name).focus();
        })
        .catch((error) => {
          // handle error
          console.log(error);
        })
    },
    submitEncounter() {
      console.log("submitEncounter");
      console.log(this);

      // validate form data
      if (this.name.length == 0) {
        $('#createEncounterName').addClass('border border-danger');
        $('#createEncounterFeedback').html('An encounter name is required!').show();
        return
      }

      // clear any warnings
      $('#createEncounterName').removeClass('border border-danger');
      $('#createEncounterFeedback').hide();
      $('#createEncounterProgress').show();

      // submit
      axios.post('/api/v1/encounters', {
        name: this.name,
        gameSystem: this.gameSystem,
        ordering: this.ordering,
        theme: this.theme
      })
        .then((response) => {
          console.log(response);
          const id = response.data.id
          window.location = `/apps/initiative/encounters/${id}`
        })
        .catch((error) => {
          console.log(error);
          $('#createEncounterProgress').hide();
          // display error to user
          $('#createEncounterFeedback').html(error).show();
        })
        .finally(() => {
        })
    }
  },
  beforeMount() {
    console.log('Fetching game systems');
    this.$store.dispatch('fetchGameSystems')
  },
  template: `
<div class="modal fade shadow p-3 rounded" id="createEncounterDialog" tabindex="-1" role="dialog" aria-labelledby="createEncounterModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title" id="createEncounterModalLabel">Create Encounter</h2>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <form>
        <div class="modal-body">
          <div class="form-group">
            <div class="input-group">
              <div class="input-group-prepend">
                <label class="input-group-text" for="createEncounterName">Name</label>
              </div>
              <input type="text" id="createEncounterName"
                     v-model="name"
                     class="form-control" aria-describedby="nameHelp" placeholder="...">
              <div class="input-group-append">
                <button id="button-random-name"
                        class="btn btn-outline-secondary input-group-text" type="button"
                        v-on:click="getRandomName">
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
                <label class="input-group-text" for="createEncounterOrdering">Ordering</label>
              </div>
              <select id="createEncounterOrdering"
                      v-model="ordering"
                      class="form-control custom-select" aria-describedby="orderingHelp">
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
                <label class="input-group-text" for="createEncounterGameSystem">Game System</label>
              </div>
              <select id="createEncounterGameSystem"
                      v-model="gameSystem"
                      class="form-control custom-select" aria-describedby="gameSystemHelp">
                <option v-for="gs in gameSystems" v-bind:value="gs.key" v-if="!gs.locked">
                  {{ gs.name }}
                </option>
              </select>
            </div>
            <small id="gameSystemHelp" class="form-text text-muted">
            A game system can be selected, which will allow the use of a health tracker
            that understands the rules of the system.
            </small>
          </div>

          <!-- errors/info -->
          <div class="form-group">
            <div class="progress" id="createEncounterProgress">
              <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
            </div>
            <div id="createEncounterFeedback" class="alert alert-danger" role="alert">
              Danger, Will Robinson!
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
          <button type="button" @click="submitEncounter" class="btn btn-primary">Create</button>
        </div>
      </form>
    </div>
  </div>
</div>
    `
}
