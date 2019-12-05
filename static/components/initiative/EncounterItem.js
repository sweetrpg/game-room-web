
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
      <p class="card-text">{{ encounter.game_system.name }} &mdash; {{ encounter.participants }} participants</p>
      <p class="card-text">
        <small class="text-muted">Last updated {{ encounter.updated_at }}</small>
      </p>
      <div class="container">
        <div class="left">
          <a href="#" class="btn btn-primary">Open</a>
        </div>
        <div class="right">
          <div class="favorite-button">
          <i class="fas fa-star"></i>
          </div>
          <div class="settings-button">
          <i class="fas fa-cog"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
`
}
