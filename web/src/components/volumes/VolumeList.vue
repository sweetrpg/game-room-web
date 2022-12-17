<template>
    <VolumeSummary v-for="volumeId in volumeIds" :id="volumeId" :key="volumeId" :volume-id="volumeId" />
</template>

<script setup>
import VolumeSummary from './VolumeSummary.vue'
defineProps({
    'volumeIds': Array,
})
</script>

<style>

</style>
