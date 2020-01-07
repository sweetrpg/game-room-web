
const GroupParticipantList = {
    name: 'group-participant-list',
    components: {
        'draggable': vuedraggable,
        'group-participant': GroupParticipant,
    },
    data() {
        return {
            isDragging: false,
        }
    },
    computed: {
        groupId() {
            console.log("get group ID for list")
            console.log(this.$store.state.group)
            return this.$store.state.group.id;
        },
        participants() {
            console.log("get participants for encounter")
            console.log(this.$store.state.group)
            if(this.$store.state.group == undefined) {
                console.log("returning empty list of participants")
                return [];
            }
            // console.log("return actual list of participants")
            // const state = this.$store.state;
            // console.log("state", state)
            // const te = state.encounter;
            // console.log("tracked encounter", te)
            const group = this.$store.state.group;
            if (group === undefined) {
                console.log("returning empty list of participants")
                return [];
            }
            console.log("group", group)
            return group.participants; // this.$store.state.encounter.encounter.participants;
        },
    },
    methods: {
    },
    beforeMount() {
        // console.log('Fetching participants');
        // this.$store.dispatch('fetchParticipants')
    },
    template: `
 <draggable class="container"
            v-model="participants" group="participants"
            @start="isDragging=true" @end="isDragging=false">
      <group-participant v-for="(p, index) in participants" :groupId="groupId" :participant="p" :key="p.id" :index="index" />
  </draggable>
`
}
