
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
  template: `
<div class="card" style="width: 18rem;">
    <img src="/static/images/encounter-default.png" class="card-img" v-bind:alt="encounter.encounter.name" />
    <div class="card-img-overlay">
        <h2 class="card-title text-white">{{ encounter.encounter.name }}</h2>
        <div class="btn-group" role="group" aria-label="Metadata group">
            <div class="btn btn-secondary favorite-button">
                <i class="fas fa-star"></i>
            </div>
            <div class="btn btn-secondary settings-button">
                <i class="fas fa-cog"></i>
            </div>
        </div>
    </div>
    <div class="card-body">
        <p class="card-text">{{ encounter.encounter.game_system.name }} &mdash; {{ encounter.encounter.participants.length }} participants</p>
        <p class="card-text">
            <small class="text-muted">Updated {{ moment(encounter.updated_at).fromNow() }}</small>
        </p>
    </div>
</div>
`
}
