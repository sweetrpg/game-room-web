
const EncounterParticipantList = {
    name: 'encounter-participant-list',
    components: {
        'encounter-participant': EncounterParticipant,
    },
    data() {
        return {
        }
    },
    computed: {
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
 <div class="container">
    <div class="row">
      <encounter-participant v-for="participant in participants" :participant="participant" :key="participant.id" />
    </div>
  </div>
`
}
