<template>
    <Event :onlyAttendedByUser="true"></Event>
</template>

<script>
import Event from "/src/components/event/Event.vue";

export default{
    components :{
        Event
    },
}
</script>