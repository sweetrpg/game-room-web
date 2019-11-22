<template>
    <div>
        <!-- <encounter-list v-model="encounters" /> -->
        <app-list />
    </div>
</template>

<script>
import AppList from '@/components/AppList'
import { mapState } from 'vuex'
export default {
    components: {
        'app-list': AppList
        },
    computed: mapState({
        encounters: (state) => state.encounters,
    }),
    beforeMount() {
        this.$store.dispatch('loadEncounters')
    },
}
</script>
