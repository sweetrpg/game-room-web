
const AddParticipantDialog = {
    name: 'add-participant-dialog',
    data: function () {
        return {
            name: '',
            type: '',
            order: 0,
            hitPoints: '',
            count: 1,
        }
    },
    computed: {
        // gameSystems: function () {
        //     return this.$store.state.gameSystems;
        // }
    },
    methods: {
        getRandomName: function () {
            console.log("getRandomName");
            axios.get('/api/v1/random/name?type=participant')
                .then((response) => {
                    console.log(response);
                    console.log(this);
                    this.name = response.data.name;
                    $('#addParticipantName').val(response.data.name).focus();
                })
                .catch((error) => {
                    // handle error
                    console.log(error);
                })
        },
        submitParticipant: function () {
            console.log("submitParticipant");
            console.log(this);

            // validate form data
            // if (this.name.length == 0) {
            //     $('#AddParticipantName').addClass('border border-danger');
            //     $('#AddParticipantFeedback').html('An encounter name is required!').show();
            //     return
            // }

            // clear any warnings
            // $('#AddParticipantName').removeClass('border border-danger');
            // $('#AddParticipantFeedback').hide();
            // $('#AddParticipantProgress').show();

            // submit
            axios.post('/api/v1/encounters/${encounterId}/participants', {
                name: this.name,
                // gameSystem: this.gameSystem,
                // ordering: this.ordering,
                // theme: this.theme
            })
                .then((response) => {
                    console.log(response);
                    const id = response.data.id
                    // window.location = `/apps/initiative/encounters/${id}`
                })
                .catch((error) => {
                    console.log(error);
                    // $('#AddParticipantProgress').hide();
                    // display error to user
                    // $('#AddParticipantFeedback').html(error).show();
                })
                .finally(() => {
                })
        }
    },
    beforeMount: function () {
        // console.log('Fetching game systems');
        // this.$store.dispatch('fetchGameSystems')
    },
    template: `
<div class="modal fade shadow p-3 rounded" id="addParticipantDialog" tabindex="-1" role="dialog" aria-labelledby="addParticipantModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="addParticipantModalLabel">Add Participant</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <form>
        <div class="modal-body">
          <div class="form-group">
            <div class="input-group">
              <div class="input-group-prepend">
                <label class="input-group-text" for="addParticipantName">Name</label>
              </div>
              <input type="text" id="addParticipantName"
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
            Enter a name for the participant.
            </small>
          </div>

<!--          <div class="form-group">
            <div class="input-group">
              <div class="input-group-prepend">
                <label class="input-group-text" for="addParticipantOrdering">Ordering</label>
              </div>
              <select id="addParticipantOrdering"
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
          </div> -->

<!--          <div class="form-group">
            <div class="input-group">
              <div class="input-group-prepend">
                <label class="input-group-text" for="addParticipantGameSystem">Game System</label>
              </div>
              <select id="addParticipantGameSystem"
                      v-model="gameSystem"
                      class="form-control custom-select" aria-describedby="gameSystemHelp">
                <option value="none" selected>None</option>
                <option v-for="gs in gameSystems" v-bind:value="gs.key">{{ gs.name }}</option>
              </select>
            </div>
            <small id="gameSystemHelp" class="form-text text-muted">
            A game system can be selected, which will allow the use of a health tracker
            that understands the rules of the system.
            </small>
          </div> -->

          <!-- errors/info -->
          <div class="form-group">
          <div class="progress" id="addParticipantProgress">
  <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
</div>
<div id="addParticipantFeedback" class="alert alert-danger" role="alert">
  Danger, Will Robinson!
</div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Done</button>
          <button type="button" @click="submitParticipant" class="btn btn-primary">Add</button>
        </div>
      </form>
    </div>
  </div>
</div>
    `
}
