
const GroupList = {
    name: 'group-list',
    components: {
        'group-item': GroupItem,
    },
    data() {
        return {
        }
    },
    computed: {
        groups() {
            return this.$store.state.groups;
        },
    },
    methods: {
    },
    beforeMount() {
        console.log('Fetching groups');
        this.$store.dispatch('fetchGroups')
    },
    template: `
 <div class="container">
    <div class="row">
      <group-item v-for="pg in groups" :group="pg" :key="pg.id" />
    </div>
  </div>
`
}
