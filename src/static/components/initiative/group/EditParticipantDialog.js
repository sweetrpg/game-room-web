
const EditParticipantDialog = {
  name: 'edit-participant-dialog',
  props: {
  },
  data() {
    return {
      participant: {},
      name: '--',
      type: 'pc',
      notes: '--',
      flags: [],
    }
  },
  computed: {
    // gameSystems: function () {
    //     return this.$store.state.gameSystems;
    // }
  },
  methods: {
    getRandomName() {
      console.log("getRandomName");
      axios.get('/api/v1/random/name?type=participant')
        .then((response) => {
          console.log(response);
          console.log(this);
          this.name = response.data.name;
          $('#editParticipantName').val(response.data.name).focus();
        })
        .catch((error) => {
          // handle error
          console.log(error);
        })
    },
    submitChanges() {

      // validate form data
      if (this.name.length == 0) {
        $('#editParticipantName').addClass('border border-danger');
        $('#editParticipantFeedback').addClass('alert-danger').removeClass('alert-success');
        $('#editParticipantFeedback').html('A participant name is required!').show();
        return
      }

      // clear any warnings
      $('#editParticipantName').removeClass('border border-danger');
      $('#editParticipantFeedback').hide();
      $('#editParticipantProgress').show();

      // submit
      const flags = (this.flags || []).filter((value) => { value !== "removed" })
      if (this.removed) {
        flags.push("removed")
      }
      axios.put(`/api/v1/groups/${this.participant.group_id}/participants/${this.participant.id}`, {
        name: this.name,
        type: this.type,
        quantity: this.quantity,
        notes: this.notes || '',
        flags: flags,
      })
        .then((response) => {
          console.log(response);
          $('#editParticipantProgress').hide();
          $('#editParticipantFeedback')
            .removeClass('alert-danger').addClass('alert-success')
            .html(`Participant updated.`).show();
          $('#editParticipantDialog').modal('hide');
          $('data#editParticipantDialogParticipantId').val('');
        })
        .catch((error) => {
          console.log(error);
          $('#editParticipantProgress').hide();
          // display error to user
          $('#editParticipantFeedback')
            .addClass('alert-danger').removeClass('alert-success')
            .html(error).show();
        })
        .finally(() => {
          this.$store.dispatch('fetchGroup')
        })
    }
  },
  watch: {
    '$store.state.currentParticipant'() {
      console.log("currentParticipant in store changed")
      this.participant = this.$store.state.currentParticipant;
      if (this.participant !== null) {
        this.name = this.participant.participant.name;
        this.type = this.participant.participant.type;
        this.order = this.participant.order;
        this.notes = this.participant.notes || '';
        this.flags = this.participant.flags || [];
        this.removed = this.flags.includes('removed')
      }
    },
  },
  beforeMount() {
    console.log('EditParticipantDialog.js beforeMount');
    // this.$store.dispatch('fetchGameSystems')
  },
  updated() {
    console.log("updated")
  },
  template: `
<div class="modal fade shadow p-3 rounded" id="editParticipantDialog" tabindex="-1" role="dialog" aria-labelledby="editParticipantModalLabel" aria-hidden="true">
  <data id="editParticipantDialogParticipantId" value=""></data>
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title" id="editParticipantModalLabel">Participant: {{ name }}</h2>
      </div>
      <div class="modal-body">

        <!-- Participant name -->
        <div class="form-group">
          <div class="input-group">
            <div class="input-group-prepend">
              <label class="input-group-text" for="editParticipantName">Name</label>
            </div>
            <input type="text" id="editParticipantName"
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
          </small>
        </div>

        <!-- Participant type -->
        <div class="form-group">
          <div class="input-group">
            <div class="input-group-prepend">
              <label class="input-group-text" for="editParticipantType">Type</label>
            </div>
            <div class="form-control">
              <div class="custom-control custom-radio custom-control-inline">
                <input type="radio" id="editParticipantTypePC" name="editParticipantType"
                        class="custom-control-input"
                        v-model="type" value="pc" />
                <label class="custom-control-label" for="editParticipantTypePC">
                  <img class="participant-type" src="/static/images/button-participant-type-pc.png" />
                  PC
                </label>
              </div>
              <div class="custom-control custom-radio custom-control-inline">
                <input type="radio" id="editParticipantTypeAdversary" name="editParticipantType"
                        class="custom-control-input"
                        v-model="type" value="adversary" />
                <label class="custom-control-label" for="editParticipantTypeAdversary">
                  <img class="participant-type" src="/static/images/button-participant-type-adversary.png" />
                  Adversary
                </label>
              </div>
              <div class="custom-control custom-radio custom-control-inline">
                <input type="radio" id="editParticipantTypeObject" name="editParticipantType"
                        class="custom-control-input"
                        v-model="type" value="object" />
                <label class="custom-control-label" for="editParticipantTypeObject">
                  <img class="participant-type" src="/static/images/button-participant-type-object.png" />
                  Object
                </label>
              </div>
            </div>
          </div>
          <small id="typeHelp" class="form-text text-muted">
          </small>
        </div>

        <!-- Options -->
        <div class="form-group">
          <div class="input-group">
            <div class="input-group-prepend">
                <span class="input-group-text">Options</span>
            </div>
          </div>
          <small id="optionsHelp" class="form-text text-muted">
          </small>
        </div>

        <!-- Notes -->
        <div class="form-group">
          <div class="input-group">
            <div class="input-group-prepend">
                <span class="input-group-text">Notes</span>
            </div>
            <textarea id="editParticipantNotes" name="notes" class="form-control"
                      aria-describedby="notesHelp" aria-label="Notes">{{ notes }}</textarea>
          </div>
          <small id="notesHelp" class="form-text text-muted">
          </small>
        </div>

        <!-- errors/info -->
        <div class="form-group">
          <div class="progress" id="editParticipantProgress">
            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
          </div>
          <div id="editParticipantFeedback" class="alert alert-danger" role="alert">
            Danger, Will Robinson!
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
        <button type="button" @click="submitChanges" class="btn btn-primary">Save</button>
      </div>
    </div>
  </div>
</div>
    `
}
