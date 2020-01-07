
const CreateGroupDialog = {
    name: 'create-group-dialog',
    data: function() {
        return {
            name: '',
        }
    },
  methods: {
    getRandomName() {
      console.log("getRandomName");
      axios.get('/api/v1/random/name?type=group')
        .then((response) => {
          console.log(response);
          console.log(this);
          this.name = response.data.name;
          $('#createGroupName').val(response.data.name).focus();
        })
        .catch((error) => {
          // handle error
          console.log(error);
        })
    },
    submitGroup() {
      console.log("submitGroup");
      console.log(this);

      // validate form data
      if (this.name.length == 0) {
        $('#createGroupName').addClass('border border-danger');
        $('#createGroupFeedback').addClass('alert-danger').html('A group name is required!').show();
        return
      }

      // clear any warnings
      $('#createGroupName').removeClass('border border-danger');
      $('#createGroupFeedback').hide();
      $('#createGroupProgress').show();

      // submit
      axios.post('/api/v1/groups', {
        name: this.name,
      })
        .then((response) => {
          console.log(response);
          const id = response.data.id
          window.location = `/apps/initiative/groups/${id}`
        })
        .catch((error) => {
          console.log(error);
          $('#createGroupProgress').hide();
          // display error to user
          $('#createGroupFeedback').html(error).show();
        })
        .finally(() => {
        })
    }
  },
      template: `
<div class="modal fade" id="createGroupDialog" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title" id="createGroupModalLabel">Create Group</h2>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <form>
        <div class="modal-body">
          <div class="form-group">
            <div class="input-group">
              <div class="input-group-prepend">
                <label class="input-group-text" for="createGroupName">Name</label>
              </div>
              <input type="text" id="createGroupName"
                     v-model="name"
                     class="form-control" aria-describedby="nameHelp" placeholder="...">
              <div class="input-group-append">
                <button id="button-random-name"
                        class="btn btn-outline-secondary input-group-text" type="button"
                        v-on:click="getRandomName">
                  <img src="/static/images/button-reset.png" alt="Random" />
                </button>
              </div>
            </div>
            <small id="nameHelp" class="form-text text-muted">
            Enter a name for the new group.
            </small>
          </div>

          <!-- errors/info -->
          <div class="form-group">
            <div class="progress" id="createGroupProgress">
              <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
            </div>
            <div id="createGroupFeedback" class="alert alert-danger" role="alert">
              Danger, Will Robinson!
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
          <button type="button" @click="submitGroup" class="btn btn-primary">Create</button>
        </div>
      </form>
    </div>
  </div>
</div>
    `
}
