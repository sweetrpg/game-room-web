
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
  <img src="/static/images/encounter-default.png" class="card-img-top" alt="..." />
  <div class="card-body">
    <h2 class="card-title">{{ encounter.name }}</h2>
    <p class="card-text">{{ encounter.game_system.name }} &mdash; {{ encounter.participants.length }} participants</p>
    <p class="card-text">
      <small class="text-muted">Last updated {{ encounter.updated_at }}</small>
    </p>
    <div class="container">
      <div class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">
        <div class="btn-group" role="group" aria-label="Action group">
          <a v-bind:href="'/apps/initiative/encounters/' + encounter.id" class="btn btn-primary">Open</a>
        </div>
        <div class="btn-group" role="group" aria-label="Separator group">
          &nbsp;
        </div>
        <div class="btn-group" role="group" aria-label="Metadata group">
          <div class="btn btn-secondary favorite-button">
            <i class="fas fa-star"></i>
          </div>
          <div class="btn btn-secondary settings-button">
            <i class="fas fa-cog"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
`
}
