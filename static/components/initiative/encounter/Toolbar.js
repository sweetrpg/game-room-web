
const EncounterToolbar = {
    name: 'encounter-toolbar',
    components: {
    },
    data() {
        return {
        };
    },
    template: `
<div>
    <div class="btn-toolbar" role="toolbar" aria-label="Encounter main toolbar">
        <div class="btn-group" role="group" aria-label="Add group">
            <button id="nextParticipant" type="button" class="btn btn-secondary"
                    data-toggle="tooltip" title="Add a participant to the encounter"
                    data-toggle="modal" data-target="#addParticipantDialog">
                <img src="/static/images/button-add-participant.png" />
            </button>
        </div>

        <div class="btn-group" role="group" aria-label="Reset group">
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="resetGroupDropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <img src="/static/images/button-reset.png" />
                </button>
                <div class="dropdown-menu" aria-labelledby="resetGroupDropdownMenuButton">
                    <a class="dropdown-item" href="#"
                       data-toggle="tooltip" title="Reset all participant initiative to 0">
                        <img src="/static/images/button-reset.png" />Reset Participants
                    </a>
                    <a class="dropdown-item" href="#"
                       data-toggle="tooltip" title="Remove all participants from the encounter except the PCs">
                        <img src="/static/images/button-clear.png" />Everything but the PCs
                    </a>
                    <a class="dropdown-item" href="#"
                       data-toggle="tooltip" data-html="true" title="Remove <em>all</em> participants from the encounter">
                        <img src="/static/images/button-clear.png" />Everything!
                    </a>
                </div>
            </div>
        </div>

        <div class="btn-group" role="group" aria-label="Encounter actions group">
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="actionsGroupDropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <img src="/static/images/button-actions.png" />
                </button>
                <div class="dropdown-menu" aria-labelledby="resetGroupDropdownMenuButton">
                    <a class="dropdown-item" href="#" title="Sort the list of participants according to their current initiative value">
                        <img src="/static/images/button-sort-participants.png" />Sort Participants
                    </a>
                    <a class="dropdown-item" href="#" title="Mark this encounter as a favorite">
                        <img src="/static/images/button-favorite-off.png" />Favorite
                    </a>
                    <a class="dropdown-item" href="#" title="Edit the encounter's settings">
                        <img src="/static/images/button-actions.png" />Encounter Settings
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
`
}
