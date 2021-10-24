
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
            console.log(this.$store.state.groups);
            return this.$store.state.groups.filter((g) => { return !g.flags.includes("tracked") });
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
    <div class="container-label text-muted">
        Groups
    </div>
    <div class="row">
        <group-item v-for="pg in groups" :group="pg" :key="pg.id" />
    </div>
  </div>
`
}
