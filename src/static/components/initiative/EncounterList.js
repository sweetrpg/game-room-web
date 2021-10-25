
const EncounterList = {
    name: 'encounter-list',
    components: {
        'encounter-item': EncounterItem,
    },
    data() {
        return {
        }
    },
    computed: {
        encounters() {
            return this.$store.state.encounters;
        },
    },
    methods: {
    },
    beforeMount() {
        console.log('Fetching encounters');
        this.$store.dispatch('fetchEncounters')
    },
    template: `
 <div class="container">
    <div class="container-label text-muted">
        Encounters
    </div>
    <div class="row">
        <encounter-item v-for="te in encounters" :encounter="te" :key="te.id" />
    </div>
  </div>
`
}
