
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
<div class="container group-participant">
    <div class="participant-image">
        <img v-if="participant.image != null"
                alt="Participant" class="img-thumbnail border shadow bg-light rounded-circle"
                v-bind:src="'data:image/png;base64,' + participant.image" />
        <img v-if="participant.image == null"
                alt="Participant" class="img-thumbnail border shadow bg-light rounded-circle"
                src="/static/images/initiative/participant-placeholder.png" />

        <div class="participant-type">
            <img v-bind:src="'/static/images/button-participant-type-' + participant.type + '.png'"
                class="text-hide float-right" />
        </div>
    </div>

    <div class="text-center participant-name">
        {{ participant.name }}
    </div>
</div>
`
}
