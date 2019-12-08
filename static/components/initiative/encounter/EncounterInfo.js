
const EncounterInfo = {
    name: 'encounter-info',
    components: {
    },
    computed: {
        encounter() {
            return this.$store.state.encounter;
        }
    },
    data() {
        return {
        };
    },
    template: `
<div class="container">
<div class="row">
<h1 class="col-8">
{{ encounter.name }}
</h1>

<div class="col text-right">
<span class="text-muted">{{ encounter.game_system.full_name }}</span>
<br />
{{ encounter.participants.length }} participant{{ encounter.participants.length == 1 ? '' : 's' }}
</div>
</div>
</div>
`
}
