
const EncounterParticipant = {
    name: 'encounter-participant',
    components: {
    },
    props: {
        encounterId: {
            type: Number,
            required: true,
        },
        participant: {
            type: Object,
            required: true,
        },
        index: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
        };
    },
    computed: {
        isCurrentTurn() {
            console.log("isCurrentTurn")
            const encounter = this.$store.state.encounter;
            console.log("encounter", encounter)
            if (encounter !== undefined &&
                encounter.session !== undefined) {
                console.log("current participant index", encounter.session.current_participant_index)
                console.log("this index", this.index)
                if (encounter.session.current_participant_index == this.index) {
                    console.log("found the one")
                    return true
                }
            }
            console.log("return false")
            return false
        }
    },
    methods: {
        getClasses() {
            var classes = 'row border rounded';
            if (this.participant.flags.includes('removed')) {
                classes += ' removed border-danger';
            }
            else {
                if (this.isCurrentTurn) {
                    classes += ' current-turn';
                }
                else {
                    classes += ' bg-light border-secondary';
                }
            }
            classes += ' encounter-participant encounter-participant-type-' + this.participant.type;

            return classes;
        },
        toggleRemoved() {
            console.log("toggleRemoved")
            if (this.participant.flags.includes('removed')) {
                const index = this.participant.flags.indexOf('removed')
                this.participant.flags.remove(index)
            }
            else {
                this.participant.flags.push('removed')
            }

            axios.put(`/api/v1/encounters/${this.participant.encounter_id}/participants/${this.participant.id}`, {
                flags: this.participant.flags,
            })
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                })
                .finally(() => {
                    this.$emit('update-participant-list')
                })
        },
        setTurn() {
            console.log("setTurn")

            axios.put(`/api/v1/encounters/${this.participant.encounter_id}/session`, {
                current_participant_index: this.index,
            })
                .then((response) => {
                    console.log(response);
                    this.$store.dispatch('setCurrentParticipant', { participant: this.participant })
                })
                .catch((error) => {
                    console.log(error);
                })
                .finally(() => {
                    this.$emit('update-participant-list')
                    this.$store.dispatch('fetchEncounter')
                })
        },
        deleteParticipant() {
            console.log("deleteParticipant")
            $('data#deleteParticipantDialogParticipantId').val(this.participant.id);
            this.$store.dispatch('setCurrentParticipant', { participant: this.participant })
            $('#deleteParticipantDialog').modal('show')
        },
        editOrder() {
            console.log("editOrder")
            $('data#editParticipantOrderDialogParticipantId').val(this.participant.id);
            this.$store.dispatch('setCurrentParticipant', { participant: this.participant })
            $('#editParticipantOrderDialog').modal('show');
        },
        editParticipant() {
            console.log("editParticipant");
            $('data#editParticipantDialogParticipantId').val(this.participant.id);
            this.$store.dispatch('setCurrentParticipant', { participant: this.participant });
            $('#editParticipantDialog').modal('show');
        },
    },
    template: `
<div v-bind:class="getClasses()">
    <div class="col-1 encounter-participant-order">
        <h4 class="text-muted" @click="editOrder">{{ participant.order }}</h4>
    </div>
    <div class="col-1 encounter-participant-type">
        <img v-bind:src="'/static/images/button-participant-type-' + participant.participant.type + '.png'"
            class="text-hide" />
    </div>
    <div class="col-7 encounter-participant-info">
        <div class="encounter-participant-name">
            <h3 @click="editParticipant">{{ participant.participant.name }}</h3>
        </div>
        <div class="encounter-participant-tags">
        </div>
    </div>
    <div class="col-1 encounter-participant-health">
    </div>
    <div class="col-1 encounter-participant-notes">
        <img src="/static/images/button-notes.png"
            v-bind:class="'notes ' + (participant.notes != null && participant.notes.length > 0 ? 'has-notes' : 'no-notes')"
            @click="editParticipant" />
    </div>
    <div class="col-1 encounter-participant-actions">
        <div class="row">
            <div class="dropdown">
                <button id="editParticipantActionsButton"
                        class="btn dropdown-toggle action-icon" type="button"
                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <img src="/static/images/button-actions.png" />
                </button>
                <div class="dropdown-menu" aria-labelledby="editParticipantActionsButton">
                    <a class="dropdown-item" @click="editParticipant">Edit...</a>
                    <a class="dropdown-item" @click="toggleRemoved">{{ participant.flags.includes('removed') ? 'Unmark' : 'Mark' }} Removed</a>
                    <a class="dropdown-item" @click="setTurn">Set Turn</a>
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item text-danger" @click="deleteParticipant">Delete</a>
                </div>
            </div>

            <div class="action-icon">
                <i class="fas fa-bars"></i>
            </div>
        </div>
    </div>
    <div class="encounter-participant-removed"
         v-if="participant.flags.includes('removed')">
    </div>
</div>
`
}
