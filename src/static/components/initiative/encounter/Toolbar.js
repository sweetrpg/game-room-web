
const EncounterToolbar = {
    name: 'encounter-toolbar',
    components: {
    },
    data() {
        return {
        };
    },
    computed: {
        encounter() {
            return this.$store.state.encounter;
        },
    },
    methods: {
        confirmResetParticipants() {
            console.log("confirmResetParticipants");
            $('#resetParticipantsConfirmationDialog').modal('show');
        },
        resetParticipants() {
            console.log("resetParticipants");

            axios.post(`/api/v1/encounters/${this.encounter.id}/participants/reset`)
                .then((response) => {
                    console.log(response);

                })
                .catch((error) => {
                    console.log(error);
                    this.$store.dispatch('addMessage', { message: error });
                    $('#resetParticipantsConfirmationDialog').modal('hide');
                })
                .finally(() => {
                    $('#resetParticipantsConfirmationDialog').modal('hide');
                    this.$emit('update-participant-list');
                    this.$store.dispatch('fetchEncounter');
                })
                    },
        confirmRemoveOthers() {
            console.log("confirmRemoveOthers");
            $('#removeOthersConfirmationDialog').modal('show');
        },
        removeOthers() {
            console.log("removeOthers");

            axios.delete(`/api/v1/encounters/${this.encounter.id}/participants?type=adversary&type=object`)
                .then((response) => {
                    console.log(response);

                })
                .catch((error) => {
                    console.log(error);
                    this.$store.dispatch('addMessage', { message: error });
                    $('#removeOthersConfirmationDialog').modal('hide');
                })
                .finally(() => {
                    $('#removeOthersConfirmationDialog').modal('hide');
                    this.$emit('update-participant-list');
                    this.$store.dispatch('fetchEncounter');
                })
        },
        confirmRemoveAll() {
            console.log("confirmRemoveAll");
            $('#removeAllConfirmationDialog').modal('show');
        },
        removeAll() {
            console.log("removeAll");

            axios.delete(`/api/v1/encounters/${this.encounter.id}/participants`)
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
                    this.$emit('update-participant-list');
                    this.$store.dispatch('fetchEncounter');
                })
        },
        sortEncounter() {
            console.log("sortEncounter");

        },
        toggleFavorite() {
            console.log("toggleFavorite");

        },
        editEncounterSettings() {
            console.log("editEncounterSettings");

        }
    },
    template: `
<div>
    <div class="btn-toolbar" role="toolbar" aria-label="Encounter main toolbar">
        <div class="btn-group" role="group" aria-label="Add group">
            <button id="addParticipant" type="button" class="btn btn-secondary"
                    data-toggle="tooltip" title="Add a participant to the encounter"
                    data-toggle="modal" data-target="#addParticipantDialog">
                <img src="/static/images/button-add-participant.png" />
            </button>
        </div>

        <div class="btn-group" role="group" aria-label="Reset group">
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="resetGroupDropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <img src="/static/images/button-reset.png" />
                </button>
                <div class="dropdown-menu" aria-labelledby="resetGroupDropdownMenuButton">
                    <a class="dropdown-item" href="#"
                       @click="confirmResetParticipants"
                       data-toggle="tooltip" title="Reset all participant initiative to 0">
                        <img src="/static/images/button-reset.png" />Reset Participant Order
                    </a>
                    <a class="dropdown-item" href="#"
                       @click="confirmRemoveOthers"
                       data-toggle="tooltip" title="Remove all participants from the encounter except the PCs">
                        <img src="/static/images/button-clear.png" />Remove everything but the PCs
                    </a>
                    <a class="dropdown-item" href="#"
                       @click="confirmRemoveAll"
                       data-toggle="tooltip" data-html="true" title="Remove <em>all</em> participants from the encounter">
                        <img src="/static/images/button-clear.png" />Remove everything!
                    </a>
                </div>
            </div>
        </div>

        <div class="btn-group" role="group" aria-label="Encounter actions group">
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="actionsGroupDropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <img src="/static/images/button-actions.png" />
                </button>
                <div class="dropdown-menu" aria-labelledby="actionsGroupDropdownMenuButton">
                    <a class="dropdown-item" href="#"
                       @click="sortEncounter"
                       title="Sort the list of participants according to their current initiative value">
                        <img src="/static/images/button-sort-participants.png" />Sort Participants
                    </a>
                    <a class="dropdown-item" href="#"
                       @click="toggleFavorite"
                       title="Mark this encounter as a favorite">
                        <img src="/static/images/button-favorite-off.png" />Favorite
                    </a>
                    <a class="dropdown-item" href="#"
                       @click="editEncounterSettings"
                       title="Edit the encounter's settings">
                        <img src="/static/images/button-actions.png" />Encounter Settings
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Dialogs -->
    <div>
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
    </div>
    <div>
        <div class="modal fade shadow p-3 rounded" id="removeOthersConfirmationDialog" tabindex="-1" role="dialog"
             aria-labelledby="removeOthersConfirmationModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Remove Non-PCs?</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>This will remove all participants from the encounter who are not player-characters. Are you sure?</p>
                        <p class="text-danger">This action cannot be undone.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-danger" @click="removeOthers">Remove</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div>
        <div class="modal fade shadow p-3 rounded" id="removeAllConfirmationDialog" tabindex="-1" role="dialog"
             aria-labelledby="removeallConfirmationModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Remove All Participants</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>This will remove all participants from the encounter. Are you sure?</p>
                        <p class="text-danger">This action cannot be undone.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-danger" @click="removeAll">Remove</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
`
}
