
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

},
createGroup() {

},
confirmDeleteEncounter() {

},
deleteEncounter() {

},
toggleFavorite() {

},
    },
  template: `
<div class="card" style="width: 18rem;"
     @click="openEncounter">
    <img src="/static/images/encounter-default.png" class="card-img" v-bind:alt="encounter.encounter.name" />
    <div class="card-img-overlay">
        <h2 class="card-title text-white">{{ encounter.encounter.name }}</h2>
        <div class="btn-group" role="group" aria-label="Metadata group">
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
