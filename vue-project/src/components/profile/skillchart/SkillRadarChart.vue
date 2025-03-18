<template>
    <div>
        <Radar v-if="loaded" :data="chartData" :options="chartOptions" />
    </div>
</template>

<script>

import { Radar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, RadialLinearScale, PointElement, LineElement, Filler } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, RadialLinearScale, PointElement, LineElement, Filler)


export default {
    components : {
        Radar,
    },
    props: {
        chartData: {
            type: Object,
            required: true
        },
        chartOptions: {
            type: Object,
            default: () => {}
        },
        loaded:{
            type: Boolean,
            default: false,
        },
    }
}
</script>