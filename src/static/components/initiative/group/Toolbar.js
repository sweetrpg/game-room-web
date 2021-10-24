
const GroupToolbar = {
    name: 'group-toolbar',
    components: {
    },
    data() {
        return {
        };
    },
    computed: {
        group() {
            return this.$store.state.group;
        },
    },
    methods: {
        confirmRemoveAll() {
            console.log("confirmRemoveAll");
            $('#removeAllConfirmationDialog').modal('show');
        },
        removeAll() {
            console.log("removeAll");

            axios.delete(`/api/v1/groups/${this.group.id}/participants`)
                .then((response) => {
                    console.log(response);

                })
                .catch((error) => {
                    console.log(error);
                    this.$store.dispatch('addMessage', { message: error });
                    $('#removeAllConfirmationDialog').modal('hide');
                })
                .finally(() => {
                    $('#removeAllConfirmationDialog').modal('hide');
                    this.$store.dispatch('fetchGroup');
                })
        },
        sortGroup() {
            console.log("sortGroup");

        },
        editGroupSettings() {
            console.log("editGroupSettings");

        }
    },
    template: `
<div>
    <div class="btn-toolbar" role="toolbar" aria-label="Group main toolbar">
        <div class="btn-group" role="group" aria-label="Add group">
            <button id="addParticipant" type="button" class="btn btn-secondary"
                    data-toggle="tooltip" title="Add a participant to the group"
                    data-toggle="modal" data-target="#addParticipantDialog">
                <img src="/static/images/button-add-participant.png" />
            </button>
        </div>

        <div class="btn-group" role="group" aria-label="Group actions group">
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="actionsGroupDropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <img src="/static/images/button-actions.png" />
                </button>
                <div class="dropdown-menu" aria-labelledby="actionsGroupDropdownMenuButton">
                    <a class="dropdown-item" href="#"
                       @click="editGroupSettings"
                       title="Edit the group's settings">
                        <img src="/static/images/button-actions.png" />Group Settings
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Dialogs -->
    <!-- div>
        <div class="modal fade shadow p-3 rounded" id="resetParticipantsConfirmationDialog" tabindex="-1" role="dialog"
             aria-labelledby="resetParticipantsConfirmationModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Reset Participant Orders</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>This will reset all participant order values to 0. Are you sure?</p>
                        <p class="text-danger">This action cannot be undone.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-danger" @click="resetParticipants">Reset</button>
                    </div>
                </div>
            </div>
        </div>
    </div -->
</div>
`
}
