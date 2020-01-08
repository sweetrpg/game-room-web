
const GroupItem = {
    name: 'group-item',
    components: {
    },
    props: {
group: {
            type: Object,
            required: true
},
expanded: {
type: Boolean
}
    },
    data() {
        return {
        }
    },
    computed: {
    },
    methods: {
    },
    beforeMount() {
    },
    template: `
<div class="card" style="width: 18rem;">
    <img src="/static/images/group-default.png" class="card-img" v-bind:alt="group.name" />
    <div class="card-img-overlay">
        <h2 class="card-title text-white">{{ group.name }}</h2>
        <div class="btn btn-secondary settings-button">
            <i class="fas fa-cog"></i>
        </div>
    </div>
    <div class="card-body">
        <p class="card-text">{{ group.participants.length }} participants</p>
        <p class="card-text">
            <small class="text-muted">Updated {{ moment(group.updated_at).fromNow() }}</small>
        </p>
    </div>
</div>
`
}
