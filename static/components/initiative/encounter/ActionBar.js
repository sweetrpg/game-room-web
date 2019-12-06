
const EncounterActionBar = {
    name: 'encounter-action-bar',
    components: {
    },
    data() {
        return {
        };
    },
    template: `
    <div class="btn-toolbar" role="toolbar" aria-label="Encounter actions toolbar">
        <div class="btn-group" role="group" aria-label="First group">
            <button id="nextParticipant" type="button" class="btn btn-secondary">
                <img src="/static/images/button-next-participant.png" />
            </button>
            <button id="collectInitiative" type="button" class="btn btn-secondary">
                <img src="/static/images/button-collect-initiative.png" />
            </button>
        </div>
    </div>
`
}
