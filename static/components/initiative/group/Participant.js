
const GroupParticipant = {
    name: 'group-participant',
    components: {
    },
    props: {
        groupId: {
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
        deleteParticipant() {
            console.log("deleteParticipant")
            $('data#deleteParticipantDialogParticipantId').val(this.participant.id);
            this.$store.dispatch('setCurrentParticipant', { participant: this.participant })
            $('#deleteParticipantDialog').modal('show')
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
</div>
`
}
