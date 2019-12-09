
const EditParticipantOrderDialog = {
  name: 'edit-participant-order-dialog',
  props: {
  },
  data() {
    return {
      participant: {},
      name: '',
      order: 0,
      position: 0,
    }
  },
  computed: {
    // gameSystems: function () {
    //     return this.$store.state.gameSystems;
    // }
  },
  methods: {
    decrementOrder() {
      this.order--;
    },
    incrementOrder() {
      this.order++;
    },
    updateDialog() {
      console.log("updateDialog")
    },
    submitChanges() {

      // validate form data
      // if (this.name.length == 0) {
      //     $('#editParticipantOrderFeedback').addClass('alert-danger').removeClass('alert-success');
      //     $('#editParticipantOrderFeedback').html('A participant name is required!').show();
      //     return
      // }

      // clear any warnings
      $('#editParticipantOrderFeedback').hide();
      $('#editParticipantOrderProgress').show();

      // submit
      axios.post(`/api/v1/encounters/${this.participant.encounter_id}/participants/${this.participant.id}`, {
        order: this.order,
      })
        .then((response) => {
          console.log(response);
          // const count = response.data.participant_ids.length;
          // window.location = `/apps/initiative/encounters/${id}`
          $('#editParticipantOrderProgress').hide();
          $('#editParticipantOrderFeedback')
            .removeClass('alert-danger').addClass('alert-success');
          // .html(`${count} participants added to encounter.`).show();
          $('#editParticipantOrderDialog').modal('hide');
          $('data#editParticipantOrderDialogParticipantId').val('');
        })
        .catch((error) => {
          console.log(error);
          $('#editParticipantOrderProgress').hide();
          // display error to user
          $('#editParticipantOrderFeedback')
            .addClass('alert-danger').removeClass('alert-success')
            .html(error).show();
        })
        .finally(() => {
          // this.$emit('update-participant-list')
        })
    }
  },
  watch: {
    '$store.state.currentParticipant'() {
      console.log("currentParticipant in store changed")
      this.participant = this.$store.state.currentParticipant;
      if (this.participant !== null) {
        this.name = this.participant.participant.name;
        this.order = this.participant.order;
      }
    },
  },
  beforeMount() {
    // console.log('Fetching game systems');
    // this.$store.dispatch('fetchGameSystems')
  },
  template: `
<div class="modal fade shadow p-3 rounded" id="editParticipantOrderDialog" tabindex="-1" role="dialog" aria-labelledby="editParticipantOrderModalLabel" aria-hidden="true">
  <data id="editParticipantOrderDialogParticipantId" value="" @onchange="updateDialog"></data>
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title" id="editParticipantOrderModalLabel">Order: {{ name }}</h2>
      </div>
      <div class="modal-body">

        <!-- initiative value -->
        <div class="form-group">
          <div class="input-group">
            <div class="input-group-prepend">
                <span class="input-group-text">Order</span>
            </div>
            <input type="number" class="form-control" name="editParticipantOrderValue"
                    v-model.number.trim="order" />
            <div class="btn-group input-group-append" role="group" aria-label="Order stepper">
              <button type="button" class="btn btn-secondary"
                      @click="decrementOrder">
                <i class="fas fa-minus"></i>
              </button>
              <button type="button" class="btn btn-secondary"
                      @click="incrementOrder">
                <i class="fas fa-plus"></i>
              </button>
            </div>
          </div>
          <small id="orderHelp" class="form-text text-muted">
          </small>
        </div>

        <!-- actual position -->
        <!-- TODO -->

        <!-- errors/info -->
        <div class="form-group">
          <div class="progress" id="editParticipantOrderProgress">
            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
          </div>
          <div id="editParticipantOrderFeedback" class="alert alert-danger" role="alert">
            Danger, Will Robinson!
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
        <button type="button" @click="submitChanges" class="btn btn-danger">Save</button>
      </div>
    </div>
  </div>
</div>
    `
}
