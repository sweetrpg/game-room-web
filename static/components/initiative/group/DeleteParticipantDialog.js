
const DeleteParticipantDialog = {
  name: 'delete-participant-dialog',
  data() {
    return {
      id: 0,
      name: '',
      type: 'pc',
    }
  },
  computed: {
  },
  methods: {
    submitDelete() {
      console.log("submitParticipant");

      // validate form data
      axios.delete(`/api/v1/groups/${this.participant.group_id}/participants/${this.participant.id}`)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        })
        .finally(() => {
          this.$emit('update-participant-list')
        })
    }
  },
  watch: {
    '$store.state.currentParticipant'() {
      console.log("currentParticipant in store changed")
      const participant = this.$store.state.currentParticipant;
      if (participant !== null) {
        this.id = participant.id;
        this.name = participant.participant.name;
        this.type = participant.participant.type;
      }
    },
  },
  beforeMount() {
    // console.log('Fetching game systems');
    // this.$store.dispatch('fetchGameSystems')
  },
  template: `
  <div class="modal fade shadow p-3 rounded" id="deleteParticipantDialog" tabindex="-1" role="dialog"
       aria-labelledby="deleteParticipantModalLabel" aria-hidden="true">
       <data id="deleteParticipantDialogParticipantId" value=""></data>
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Delete Participant</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <img v-bind:src="'/static/images/button-participant-type-' + type + '.png'"
            class="text-hide" />
        <p>Are you sure you want to delete {{ name }}?</p>
        <p class="text-danger>This action cannot be undone.</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-danger">Delete</button>
      </div>
    </div>
  </div>
</div>
    `
}
