<!-- <template>
    <div id="legend">
        <div v-for="item in legendItems" :key="item.label">
            <div
                :style="{ background: item.color, border: `2px solid ${item.borderColor}`, width: '20px', height: '20px' }">
            </div>
            {{ item.label }}
        </div>
    </div>
</template> -->

<template>
    <div id="map-container" class="relative h-full w-full">
        <div class="absolute top-4 right-4 bg-white bg-opacity-80 p-4 rounded-md z-20 flex flex-col">
            <div v-for="(item, index) in legendItems" :key="item.label">
                <label>
                    <input type="checkbox" v-model="item.showLayer" />
                    <div
                        :style="{ background: item.color, border: `2px solid ${item.borderColor}`, width: '20px', height: '20px' }">
                    </div>
                    {{ item.label }}
                </label>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    props: {
        legendItems: Array
    }
}
</script>

<style scoped>
#legend div {
    display: flex;
    align-items: center;
}

#legend div div {
    margin-right: 5px;
}
</style>