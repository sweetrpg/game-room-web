
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
        }
    },
    data() {
        return {
        };
    },
    methods: {
        editOrder() {
            console.log("editOrder")
            $('data#editParticipantOrderDialogParticipantId').val(this.participant.id);
            this.$store.dispatch('setCurrentParticipant', { participant: this.participant })
            $('#editParticipantOrderDialog').modal('show');
        },
        editParticipant() {
            console.log("editParticipant")
            $('data#editParticipantDialogParticipantId').val(this.participant.id);
            this.$store.dispatch('setCurrentParticipant', { participant: this.participant })
            $('#editParticipantDialog').modal('show')
        },
    },
    template: `
<div class="encounter-participant row border border-secondary rounded bg-light">
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
            <div class="action-icon" @click="editParticipant">
                <img src="/static/images/button-actions.png" />
            </div>
            <div class="action-icon">
                <i class="fas fa-bars"></i>
            </div>
        </div>
    </div>
</div>
`
}
