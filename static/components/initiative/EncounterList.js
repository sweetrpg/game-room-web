
const EncounterList = {
    name: 'encounter-list',
    components: {
        'encounter-item': EncounterItem,
    },
    data: function () {
        return {
        }
    },
    computed: {
        encounters: function () {
            return this.$store.state.encounters;
        },
    },
    methods: {
    },
    beforeMount: function () {
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
