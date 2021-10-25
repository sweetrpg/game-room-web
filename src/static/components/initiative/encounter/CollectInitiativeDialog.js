
const CollectInitiativeDialog = {
    name: 'collect-initiative-dialog',
    components: {
    },
    data() {
        return {
            index: 0,
            id: null,
            name: '',
            typeName: '',
            value: 0,
            count: 0,
            participant: null,
            collectedValues: {},
        };
    },
    methods: {
        updateParticipantInfo() {
            console.log("updateParticipantInfo", this.index, this.participant);
            if (this.participant !== null && this.index >= 0) {
                this.id = this.participant.id;

                if (this.collectedValues[this.id] === undefined ||
                    this.collectedValues[this.id] === null) {
                    this.collectedValues[this.id] = this.participant.order || 0;
                }

                this.name = this.participant.participant.name;
                this.typeName = participantTypeMap[this.participant.participant.type];
                this.value = this.collectedValues[this.id];
            }
            else {
                console.log("current participant is not set or index is invalid")
            }
        },
        storeValue() {
            if (this.id !== null) {
                this.collectedValues[this.id] = $('input#collectInitiativeValue').val();
            }
        },
        checkCollection() {
            console.log("checking collected values")

            const collectedCount = Object.keys(this.collectedValues).length;
            if (collectedCount == this.count) {
                $('#collectInitiativeFeedback')
                    .addClass('alert-success')
                    .html("All initiative values have been collected.").show();
            }
        },
        doneCollecting() {
            console.log("doneCollecting");

            this.storeValue();

            // clear any warnings
            $('#collectInitiativeFeedback').hide();
            $('#collectInitiativeProgress').show();

            axios.put(`/api/v1/encounters/${this.participant.encounter_id}/order`, {
                ...this.collectedValues
            })
                .then((response) => {
                    console.log(response);

                    $('#collectInitiativeDialog').modal('hide');
                    this.collectedValues = {};
                })
                .catch((error) => {
                    console.log(error);
                    $('#collectInitiativeProgress').hide();
                    // display error to user
                    $('#collectInitiativeFeedback')
                        .addClass('alert-danger').removeClass('alert-success')
                        .html(error).show();
                })
                .finally(() => {
                    this.$emit('update-participant-list')
                    this.$store.dispatch('fetchEncounter')
                })

        },
        previousParticipant() {
            console.log("previousParticipant")

            this.storeValue();

            this.index -= 1;
            if (this.index < 0) {
                this.index = this.count;
            }

            this.checkCollection();
            this.$store.dispatch('setCurrentParticipant', { index: this.index })

            $('#collectInitiativeValue').focus();
        },
        nextParticipant() {
            console.log("nextParticipant")

            this.storeValue();

            this.index += 1;
            if (this.index >= this.count) {
                this.index = 0;
            }

            this.checkCollection();
            this.$store.dispatch('setCurrentParticipant', { index: this.index })

            $('#collectInitiativeValue').focus();
        },
    },
    watch: {
        '$store.state.encounter'() {
            console.log("encounter in store changed")
            if (this.$store.state.encounter === undefined ||
                this.$store.state.encounter.encounter === undefined ||
                this.$store.state.encounter.encounter.participants === undefined) {
                return
            }

            const participantList = this.$store.state.encounter.encounter.participants;
            console.log(participantList);
            this.count = participantList.length;
        },
        '$store.state.currentParticipantIndex'() {
            this.index = this.$store.state.currentParticipantIndex;
            this.updateParticipantInfo();
        },
        '$store.state.currentParticipant'() {
            console.log("currentParticipant in store changed")
            this.participant = this.$store.state.currentParticipant;
            this.updateParticipantInfo();
        },
        // 'value'() {
        //     console.log("local value changed");
        //     this.storeValue();
        // }
    },
    template: `
<div class="modal fade shadow p-3 rounded" id="collectInitiativeDialog" tabindex="-1" role="dialog" aria-labelledby="collectInitiativeModalLabel" aria-hidden="true">
  <data id="collectInitiativeDialogParticipantId" value=""></data>
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title" id="collectInitiativeModalLabel">Collecting Initiative</h2>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">

        <!-- Participant name -->
        <div class="form-group">
          <div class="input-group collect-initiative-name">
          <span class="value">{{ name }}</span>
          </div>
          <small id="nameHelp" class="form-text text-muted">
          </small>
        </div>

        <!-- Participant type -->
        <div class="form-group">
          <div class="input-group text-muted collect-initiative-type">
          <span class="value">{{ typeName }}</span>
          </div>
          <small id="typeHelp" class="form-text text-muted">
          </small>
        </div>

        <!-- Value -->
        <div class="form-group">
          <div class="input-group">
            <input type="number" class="form-control collect-initiative"
                   id="collectInitiativeValue" name="collectInitiativeValue"
                    v-model.number.trim="value" />
          </div>
          <small id="valueHelp" class="form-text text-muted">
          </small>
        </div>

        <!-- Prev/next buttons -->
        <div class="form-group">
            <div class="btn-group advancement-buttons" role="group" aria-label="Advancement buttons">
                <button type="button" class="btn btn-secondary" @click="previousParticipant">Previous</button>
                <button type="button" class="btn btn-secondary" @click="nextParticipant">Next</button>
            </div>
        </div>

        <!-- errors/info -->
        <div class="form-group">
          <div class="progress" id="collectInitiativeProgress">
            <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
          </div>
          <div id="collectInitiativeFeedback" class="alert" role="alert">
            Danger, Will Robinson!
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button type="button" @click="doneCollecting" class="btn btn-primary">Done</button>
      </div>
    </div>
  </div>
</div>
`
}
