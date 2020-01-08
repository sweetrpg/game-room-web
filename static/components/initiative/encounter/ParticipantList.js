
const EncounterParticipantList = {
    name: 'encounter-participant-list',
    components: {
        'draggable': vuedraggable,
        'encounter-participant': EncounterParticipant,
    },
    data() {
        return {
            isDragging: false,
        }
    },
    computed: {
        encounterId() {
            console.log("get encounter ID for list")
            console.log(this.$store.state.encounter)
            return this.$store.state.encounter.id;
        },
        participants() {
            console.log("get participants for encounter")
            console.log(this.$store.state.encounter)
            if(this.$store.state.encounter == undefined) {
                console.log("returning empty list of participants")
                return [];
            }
            // console.log("return actual list of participants")
            // const state = this.$store.state;
            // console.log("state", state)
            // const te = state.encounter;
            // console.log("tracked encounter", te)
            const encounter = this.$store.state.encounter.encounter;
            if(encounter === undefined) {
                console.log("returning empty list of participants")
                return [];
            }
            console.log("encounter", encounter)
            return encounter.participants; // this.$store.state.encounter.encounter.participants;
        },
    },
    methods: {
    },
    beforeMount() {
        // console.log('Fetching participants');
        // this.$store.dispatch('fetchParticipants')
    },
    template: `
<div>
    <div class="text-center" v-if="participants.length == 0">
        <h2 class="text-muted">No participants</h2>
        <h5>(Add some by clicking the helmet in the upper-left corner.)</h5>
    </div>
    <draggable class="container" v-if="participants.length > 0"
               v-model="participants" group="participants"
               @start="isDragging=true" @end="isDragging=false">
        <encounter-participant v-for="(p, index) in participants" :encounterId="encounterId" :participant="p" :key="p.id" :index="index" />
    </draggable>
</div>
`
}
