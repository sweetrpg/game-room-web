
const DeleteGroupDialog = {
    name: 'delete-group-dialog',
    data() {
        return {
            id: 0,
            name: '',
        }
    },
    computed: {
    },
    methods: {
        submitDelete() {
            console.log("submitDelete");

            // validate form data
            axios.delete(`/api/v1/groups/${this.id}`)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                })
                .finally(() => {
                })
        }
    },
    watch: {
    },
    beforeMount() {
        // console.log('Fetching game systems');
        // this.$store.dispatch('fetchGameSystems')
    },
    template: `
  <div class="modal fade shadow p-3 rounded" id="deleteGroupDialog" tabindex="-1" role="dialog"
       aria-labelledby="deleteGroupModalLabel" aria-hidden="true">
       <data id="deleteGroupDialogGroupId" value=""></data>
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Delete Group</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>Are you sure you want to delete the group '{{ name }}'?</p>
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
