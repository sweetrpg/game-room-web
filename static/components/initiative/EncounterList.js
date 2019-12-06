
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
    <div class="row">
      <encounter-item v-for="encounter in encounters" :encounter="encounter" :key="encounter.id" />
    </div>
  </div>
`
}
