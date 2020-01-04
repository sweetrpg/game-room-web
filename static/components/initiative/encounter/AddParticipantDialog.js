
const AddParticipantDialog = {
  name: 'add-participant-dialog',
  data() {
    return {
      name: '',
      type: 'pc',
      order: 0,
      health: '',
      quantity: 1,
      notes: '',
    }
  },
  computed: {
    // gameSystems: function () {
    //     return this.$store.state.gameSystems;
    // }
  },
  methods: {
    incrementQuantity() {
      this.quantity += 1
      if (this.quantity > 100) {
        this.quantity = 100
      }
      $('#addParticipantQuantity').focus();
    },
    decrementQuantity() {
      this.quantity -= 1
      if (this.quantity < 1) {
        this.quantity = 1
      }
      $('#addParticipantQuantity').focus();
    },
    getRandomName() {
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
    submitParticipant() {
      console.log("submitParticipant");
      console.log(this);

      // validate form data
      if (this.name.length == 0) {
          $('#addParticipantName').addClass('border border-danger');
          $('#addParticipantFeedback').addClass('alert-danger').removeClass('alert-success');
          $('#addParticipantFeedback').html('A participant name is required!').show();
          return
      }

      // clear any warnings
      $('#addParticipantName').removeClass('border border-danger');
      $('#addParticipantFeedback').hide();
      $('#addParticipantProgress').show();

      // submit
      const encounterId = $('data#encounterId').val()
      axios.post(`/api/v1/encounters/${encounterId}/participants`, {
        name: this.name,
        type: this.type,
        order: this.order,
        quantity: this.quantity,
        health: this.health,
        notes: this.notes,
      })
        .then((response) => {
          console.log(response);
          const count = response.data.participant_ids.length;
          // window.location = `/apps/initiative/encounters/${id}`
          $('#addParticipantProgress').hide();
          $('#addParticipantFeedback')
            .removeClass('alert-danger').addClass('alert-success')
            .html(`${count} participants added to encounter.`).show();
        })
        .catch((error) => {
          console.log(error);
          $('#addParticipantProgress').hide();
          // display error to user
          $('#addParticipantFeedback')
            .addClass('alert-danger').removeClass('alert-success')
            .html(error).show();
        })
        .finally(() => {
          this.$emit('update-participant-list')
          this.$store.dispatch('fetchEncounter')
        })
    }
  },
  beforeMount() {
    // console.log('Fetching game systems');
    // this.$store.dispatch('fetchGameSystems')
  },
  template: `
<div class="modal fade shadow p-3 rounded" id="addParticipantDialog" tabindex="-1" role="dialog" aria-labelledby="addParticipantModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title" id="addParticipantModalLabel">Add Participant</h2>
      </div>
      <div class="modal-body">
        <div>
          <!-- Nav tabs -->
          <ul class="nav nav-tabs">
            <li class="nav-item">
              <a id="add-participant-enter-tab" class="nav-link active"
                data-toggle="tab" href="#add-participant-enter" role="tab"
                aria-controls="add-participant-enter" aria-selected="true">
                Enter
              </a>
            </li>
            <li class="nav-item">
              <a id="add-participant-group-tab" class="nav-link"
                data-toggle="tab" href="#add-participant-group" role="tab"
                aria-controls="add-participant-group" aria-selected="false">
                Group
              </a>
            </li>
            <li class="nav-item">
              <a id="add-participant-special-tab" class="nav-link"
                data-toggle="tab" href="#add-participant-special" role="tab"
                aria-controls="add-participant-special" aria-selected="false">
                Special
              </a>
            </li>
          </ul>
        </div>

        <p/>

        <!-- Tab panes -->
        <div class="tab-content">
          <div class="tab-pane fade show active" id="add-participant-enter" role="tabpanel"
                aria-labelledby="add-participant-enter-tab">
            <!-- Participant name -->
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
                          v-on:click="getRandomName"
                          data-toggle="tooltip"
                          title="Generate a random name and fill it in">
                    <img src="/static/images/button-reset.png" alt="Random" />
                  </button>
                </div>
              </div>
              <small id="nameHelp" class="form-text text-muted">
              Enter a name for the participant.
              </small>
            </div>

            <!-- Participant type -->
            <div class="form-group">
              <div class="input-group">
                <div class="input-group-prepend">
                  <label class="input-group-text" for="addParticipantType">Type</label>
                </div>
                <div class="form-control">
                  <div class="custom-control custom-radio custom-control-inline">
                    <input type="radio" id="participantTypePC" name="addParticipantType"
                            class="custom-control-input"
                            v-model="type" value="pc" />
                    <label class="custom-control-label" for="participantTypePC">
                      <img class="participant-type" src="/static/images/button-participant-type-pc.png" />
                      PC
                    </label>
                  </div>
                  <div class="custom-control custom-radio custom-control-inline">
                    <input type="radio" id="participantTypeAdversary" name="addParticipantType"
                            class="custom-control-input"
                            v-model="type" value="adversary" />
                    <label class="custom-control-label" for="participantTypeAdversary">
                      <img class="participant-type" src="/static/images/button-participant-type-adversary.png" />
                      Adversary
                    </label>
                  </div>
                  <div class="custom-control custom-radio custom-control-inline">
                    <input type="radio" id="participantTypeObject" name="addParticipantType"
                            class="custom-control-input"
                            v-model="type" value="object" />
                    <label class="custom-control-label" for="participantTypeObject">
                      <img class="participant-type" src="/static/images/button-participant-type-object.png" />
                      Object
                    </label>
                  </div>
                </div>
              </div>
              <small id="typeHelp" class="form-text text-muted">
              Setting the type of the participant will hellp the tracker in managing the encounter.
              </small>
            </div>

            <!-- Quantity -->
            <div class="form-group">
              <div class="input-group">
                <div class="input-group-prepend">
                  <label class="input-group-text" for="addParticipantQuantity">Quantity</label>
                </div>
                <input type="number" class="form-control" name="addParticipantQuantity"
                        v-model.number.trim="quantity" />
                <div class="btn-group input-group-append" role="group" aria-label="Quantity stepper">
                  <button type="button" class="btn btn-secondary"
                          @click="decrementQuantity">
                    <i class="fas fa-minus"></i>
                  </button>
                  <button type="button" class="btn btn-secondary"
                          @click="incrementQuantity">
                    <i class="fas fa-plus"></i>
                  </button>
                </div>
              </div>
              <small id="quantityHelp" class="form-text text-muted">
              How many of this participant do you want to add?
              </small>
            </div>

            <!-- Health -->
            <div class="form-group">
              <div class="input-group">
                <div class="input-group-prepend">
                  <label class="input-group-text" for="addParticipantHealth">Health</label>
                </div>
                <input type="text" class="form-control" name="addParticipantHealth"
                        placeholder="HP[/Max[/Temp]]"
                        v-model.trim="health" />
              </div>
              <small id="healthHelp" class="form-text text-muted">
              Enter the current hit points, and optionally maximum and then temporary hit
              points, separated, by slashes ('/'). Omitting the maximum hit point value
              will cause it to be set to the current value. Omitting the temporary hit point
              value will cause it to be set to 0.
              </small>
            </div>

            <!-- Notes -->
            <div class="form-group">
              <div class="input-group">
                <div class="input-group-prepend">
                    <span class="input-group-text">Notes</span>
                </div>
                <textarea id="addParticipantNotes" name="notes" class="form-control"
                          aria-describedby="notesHelp" aria-label="Notes">{{ notes }}</textarea>
              </div>
              <small id="notesHelp" class="form-text text-muted">
              </small>
            </div>

          </div>

          <div class="tab-pane fade" id="add-participant-group" role="tabpanel"
                aria-labelledby="add-participant-group-tab">
                TODO: group list
          </div>

          <div class="tab-pane fade" id="add-participant-special" role="tabpanel"
                aria-labelledby="add-participant-special-tab">
                TODO: lair actions, etc.
          </div>
        </div>

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
    </div>
  </div>
</div>
    `
}
