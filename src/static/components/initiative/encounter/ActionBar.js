
const EncounterActionBar = {
    name: 'encounter-action-bar',
    components: {
    },
    data() {
        return {
        };
    },
    computed: {
        encounter() {
            return this.$store.state.encounter;
        },
        canAdvance() {
            const encounter = this.$store.state.encounter;
            if (encounter !== undefined &&
                encounter.encounter !== undefined &&
                encounter.encounter.participants.length > 1) {
                return true
            }
            return false
        },
        canCollect() {
            const encounter = this.$store.state.encounter;
            if (encounter !== undefined &&
                encounter.encounter !== undefined &&
                encounter.encounter.participants.length > 0) {
                return true
            }
            return false
        },
    },
    methods: {
        nextParticipant() {
            const session = this.encounter.session;
            if (session) {
                console.log("got a session", session)

                axios.post(`/api/v1/encounters/${this.encounter.id}/next`)
                    .then((response) => {
                        console.log(response);

                        const nextIndex = response.data.index;
                        console.log(nextIndex);

                        if (nextIndex >= 0) {
                            axios.put(`/api/v1/encounters/${this.encounter.id}/session`, {
                                current_participant_index: nextIndex,
                            })
                                .then((response) => {
                                    console.log(response);
                                })
                                .catch((error) => {
                                    console.log(error);
                                    this.$store.dispatch('addMessage', { message: error })
                                })
                                .finally(() => {
                                    this.$emit('update-participant-list')
                                    this.$store.dispatch('fetchEncounter')
                                })
                        }
                        else {
                            this.$store.dispatch('addMessage', { message: "There are no participants left.", type: 'warning' })
                        }
                    })
                    .catch((error) => {
                        console.log(error);
                        this.$store.dispatch('addMessage', { message: error })
                    })
                    .finally(() => {
                        // this.$emit('update-participant-list')
                        // this.$store.dispatch('fetchEncounter')
                    })

                if (session.current_participant_index === null) {
                    session.current_participant_index = 0
                }
                else {
                    session.current_participant_index++
                }

            }
        },
        collectInitiative() {
            console.log("collectInitiative", this.encounter)
            if(this.encounter.encounter.participants.length == 0) {
                console.log("No participant in this encounter");
                return;
            }
            const firstParticipant = this.encounter.encounter.participants[0];
            console.log(firstParticipant)
            // $('data#editParticipantOrderDialogParticipantId').val(this.participant.id);
            this.$store.dispatch('setCurrentParticipant', { participant: firstParticipant })
            $('#collectInitiativeDialog').modal('show');
        },
    },
    watch: {
        'this.$store.state.encounter'() {
            console.log("$store encounter updated");
        },
    },
    template: `
    <div class="btn-toolbar" role="toolbar" aria-label="Encounter actions toolbar">
        <div class="btn-group" role="group" aria-label="First group">
            <button id="nextParticipant" type="button"
                    :class="'btn btn-secondary ' + (canAdvance ? '' : 'disabled')"
                    @click="nextParticipant">
                <img src="/static/images/button-next-participant.png" />
            </button>
            <button id="collectInitiative" type="button"
                    :class="'btn btn-secondary ' + (canCollect ? '' : 'disabled')"
                    @click="collectInitiative">
                <img src="/static/images/button-collect-initiative.png" />
            </button>
        </div>
    </div>
`
}
