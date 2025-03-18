<template>
    <div>
        <Bar v-if="loaded"
            :data="chartData"
            :options="chartOptions" 
            :width="width"
            :height="height"
        />
    </div>
</template>

<script>

import {  Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, RadialLinearScale, PointElement, LineElement, Filler } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, RadialLinearScale, PointElement, LineElement, Filler)


export default {
    components : {
        Bar,
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
        width: {
            type: Number,
            default: 400
        },
        height: {
            type: Number,
            default: 400
        },
    }
}
</script>