
const EncounterItem = {
    name: 'encounter-item',
    components: {
    },
    props: {
        encounter: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
        };
    },
    methods: {
        openEncounter() {
            console.log("openEncounter");
            window.location = `/apps/initiative/encounters/${this.encounter.id}`
        },
        createGroup() {
            console.log("createGroup");

        },
        confirmDeleteEncounter() {
            console.log("confirmDeleteEncounter");
            $('#deleteEncounterDialogEncounterId').val(this.encounter.id);
            $('#deleteEncounterDialog').show();
        },
        toggleFavorite() {
            console.log("toggleFavorite");
            var flags = this.encounter.flags;
            console.log("flags", flags);
            if (flags.includes("favorite")) {
                _.pull(flags, "favorite")
            }
            else {
                flags.push("favorite")
            }
            console.log("flags", flags);
            axios.put(`/api/v1/encounters/${this.encounter.id}`, {
                flags: flags,
            })
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
    },
    template: `
<div class="card" style="width: 18rem;">
    <img src="/static/images/encounter-default.png" class="card-img" v-bind:alt="encounter.encounter.name" />
    <div class="card-img-overlay">
        <h2 class="card-title text-white">{{ encounter.encounter.name }}</h2>
        <div class="btn-group" role="group" aria-label="Metadata group">
            <div class="btn btn-primary open-button" @click="openEncounter">
                <i class="fas fa-play"></i>
            </div>
            <div class="btn btn-secondary favorite-button"
                 @click="toggleFavorite">
                <i v-bind:class="'fa' + (encounter.encounter.flags.includes('favorite') ? 's' : 'r') + ' fa-star'"></i>
            </div>
            <div class="btn-group" role="group">
                <button v-bind:id="'actionsButtonEncounter' + encounter.id" type="button"
                        class="btn btn-secondary dropdown-toggle settings-button"
                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i class="fas fa-cog"></i>
                </button>
                <div class="dropdown-menu" v-bind:aria-labelledby="'actionsButtonEncounter' + encounter.id">
                    <a class="dropdown-item" @click="openEncounter">Open...</a>
                    <a class="dropdown-item" @click="createGroup">Create group</a>
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item text-danger" @click="confirmDeleteEncounter">Delete</a>
                </div>
            </div>
        </div>
    </div>
    <div class="card-body">
        <p class="card-text">{{ encounter.encounter.game_system.name }} &mdash; {{ encounter.encounter.participants.length }} participants</p>
        <p class="card-text">
            <small class="text-muted">Updated {{ moment.utc(encounter.updated_at).fromNow() }}</small>
        </p>
    </div>
</div>
`
}
