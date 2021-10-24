
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
        editGroup() {
            console.log("editGroup");
            window.location = `/apps/initiative/groups/${this.group.id}`
        },
        createEncounter() {
            console.log("createEncounter")
            axios.post(`/api/v1/groups/from/${this.encounter.id}`)
                .then((response) => {
                    console.log(response);
                    window.location.reload();
                })
                .catch((error) => {
                    console.log(error);
                })
                .finally(() => {
                })
        },
        confirmDeleteGroup() {
            console.log("confirmDeleteGroup");
            $('#deleteGroupDialogGroupId').val(this.group.id);
            $('#deleteGroupDialog').show();
        }
    },
    beforeMount() {
    },
    template: `
<div class="card" style="width: 18rem;">
    <img src="/static/images/group-default.png" class="card-img" v-bind:alt="group.name" />
    <div class="card-img-overlay">
        <h2 class="card-title text-white">{{ group.name }}</h2>
        <div class="btn-group" role="group">
            <button v-bind:id="'actionsButtonGroup' + group.id" type="button"
                    class="btn btn-secondary dropdown-toggle settings-button"
                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-cog"></i>
            </button>
            <div class="dropdown-menu" v-bind:aria-labelledby="'actionsButtonGroup' + group.id">
                <a class="dropdown-item" @click="editGroup">Edit...</a>
                <a class="dropdown-item" @click="createEncounter">Create encounter</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item text-danger" @click="confirmDeleteGroup">Delete</a>
            </div>
        </div>
    </div>
    <div class="card-body">
        <p class="card-text">{{ group.participants.length }} participants</p>
        <p class="card-text">
            <small class="text-muted">Updated {{ moment.utc(group.updated_at).fromNow() }}</small>
        </p>
    </div>
</div>
`
}
