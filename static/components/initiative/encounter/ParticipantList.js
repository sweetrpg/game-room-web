
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
            return this.$store.state.encounter.id;
        },
        participants() {
            return this.$store.state.encounter.participants;
        },
    },
    methods: {
    },
    beforeMount() {
        console.log('Fetching participants');
        // this.$store.dispatch('fetchParticipants')
    },
    template: `
 <draggable class="container"
            v-model="participants" group="participants"
            @start="isDragging=true" @end="isDragging=false">
      <encounter-participant v-for="p in participants" :encounterId="encounterId" :participant="p" :key="p.id" />
  </draggable>
`
}
