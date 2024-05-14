<template>
  <div id="map-container" class="relative w-full h-full">
    <Legend :legendItems="legendItems" class="absolute z-20 p-4 bg-white rounded-md top-4 right-4 bg-opacity-80" />

    <v-slide-group>
      <v-slide-item v-for="(date, index) in dates" :key="index" @click="selectDate(date)"
        class="p-4 text-center rounded-lg shadow-md cursor-pointer">
        <v-card :color="date === selectedDate ? 'blue' : ''" class="px-2 py-1 mx-2 my-2" dark>
          <p class="text-2xl">{{ date }}</p>
        </v-card>
      </v-slide-item>
    </v-slide-group>

    <div id="map"></div>
  </div>
</template>


<script lang="ts">
import Feature from 'ol/Feature';
import Map from 'ol/Map';
import Overlay from 'ol/Overlay';
import View from 'ol/View';
import GeoJSON from 'ol/format/GeoJSON';
import { Polygon } from 'ol/geom';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
import { fromLonLat } from 'ol/proj';
import { OSM } from 'ol/source';
import VectorSource from 'ol/source/Vector';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import Style from 'ol/style/Style';
import { watch } from 'vue';
import { useStore } from 'vuex';
import Legend from './Legend.vue';

export default {
  components: {
    Legend
  },

  data() {
    return {
      legendItems: [
        {
          //green with 50% opacity
          color: 'rgba(0, 255, 0, 0.5)',
          borderColor: '#00ff00',
          label: 'Območje zelo redkih poplav',
          showLayer: true
        },
        {
          //orange with 50% opacity
          color: 'rgba(255, 165, 0, 0.5)',
          borderColor: '#FFA500',
          label: 'Območje redkih poplav',
          showLayer: true
        },
        {
          //red with 50% opacity
          color: 'rgba(255, 0, 0, 0.5)',
          // red border
          borderColor: '#ff0000',
          label: 'Območje pogostih poplav',
          showLayer: true
        },
        // add more items as needed
      ],
      dates: [],
      vectorLayerArea1: new VectorLayer({
        source: new VectorSource(),
      }),
      vectorLayerArea2: new VectorLayer({
        source: new VectorSource(),
      }),
      VectorLayerArea3: new VectorLayer({
        source: new VectorSource(),
      }),
      VectorLayerArea4: new VectorLayer({
        source: new VectorSource(),
      }),
      VectorLayerArea5: new VectorLayer({
        source: new VectorSource(),
      }),

    }
  },
  mounted() {

    watch(() => this.legendItems[0].showLayer, (newVal) => {
      vectorLayer.setVisible(newVal);
    });

    watch(() => this.legendItems[1].showLayer, (newVal) => {
      vectorLayer2.setVisible(newVal);
    });

    watch(() => this.legendItems[2].showLayer, (newVal) => {
      vectorLayer3.setVisible(newVal);
    });

    // Create a vector source to load the GeoJSON data

    const vectorSourceZeloRedke = new VectorSource({
      url: '././data/DRSV_OPKP_ZR_POPL.json',
      format: new GeoJSON(),
    });

    const vectorSourceRedke = new VectorSource({
      url: '././data/DRSV_OPKP_REDKE_POPL.json',
      format: new GeoJSON(),
    });

    const vectorSourcePogoste = new VectorSource({
      url: '././data/DRSV_OPKP_POGOSTE_POPL.json',
      format: new GeoJSON(),
    });


    // Create a style for the vector layer
    const vectorStyle = new Style({
      fill: new Fill({
        // green with 50% opacity
        color: 'rgba(0, 255, 0, 0.5)',
      }),
      stroke: new Stroke({
        color: '#00ff00', // green
        width: 2,
      }),
    });

    const vectorStyle2 = new Style({
      fill: new Fill({
        // orange with 50% opacity
        color: 'rgba(255, 165, 0, 0.5)',
      }),
      stroke: new Stroke({
        color: "#FFA500", // orange
        width: 2,
      }),
    });

    const vectorStyle3 = new Style({
      fill: new Fill({
        // red with 50% opacity
        color: 'rgba(255, 0, 0, 0.5)',
      }),
      stroke: new Stroke({
        color: '#ff0000', // red
        width: 2,
      }),
    });

    // Create a vector layer to display the GeoJSON data
    const vectorLayer = new VectorLayer({
      source: vectorSourceZeloRedke,
      style: vectorStyle,
    });

    const vectorLayer2 = new VectorLayer({
      source: vectorSourceRedke,
      style: vectorStyle2,
    });

    const vectorLayer3 = new VectorLayer({
      source: vectorSourcePogoste,
      style: vectorStyle3,
    });

    // area poplavljanja
    // Define the polygon coordinates
    const coordinates1 = [
      [14.7172623, 46.4869874],
      [14.7007828, 46.4510451],
      [14.607399, 46.4377973],
      [14.5826798, 46.3809841],
      [14.6458512, 46.3127303],
      [14.8161393, 46.3127303],
      [15.0111466, 46.3146274],
      [15.1127701, 46.3525554],
      [15.1869278, 46.4037165],
      [15.1759415, 46.4586139],
      [15.1347428, 46.5021139],
      [14.8930436, 46.5153462],
      [14.7172623, 46.4869874]
    ].map(coord => fromLonLat(coord));

    // Create the polygon geometry
    const polygon1 = new Polygon([coordinates1]);

    // Create a feature and set the geometry
    const feature = new Feature({
      geometry: polygon1
    });

    const vectorSource1 = new VectorSource({
      features: [feature]
    });

    // Create a vector layer and add the source
    this.vectorLayerArea1 = new VectorLayer({
      source: vectorSource1
    });



    const coordinates2 = [
      [14.4607489, 46.2275624],
      [14.3783514, 46.1657752],
      [14.3865912, 46.0886817],
      [14.522547, 46.0705824],
      [14.6543829, 46.0696296],
      [14.6791021, 46.1229588],
      [14.6543829, 46.188597],
      [14.5774786, 46.2256622],
      [14.4607489, 46.2275624]
    ].map(coord => fromLonLat(coord));

    // Create the polygon geometry
    const polygon2 = new Polygon([coordinates2]);

    // Create a feature and set the geometry
    const feature2 = new Feature({
      geometry: polygon2
    });

    const vectorSource2 = new VectorSource({
      features: [feature2]
    });

    // Create a vector layer and add the source
    this.vectorLayerArea2 = new VectorLayer({
      source: vectorSource2,

    });



    const coordinates3 = [
      [15.2602685, 46.2683542],
      [15.2101433, 46.2671675],
      [15.1847375, 46.2367799],
      [15.1843941, 46.2085137],
      [15.2125466, 46.1982964],
      [15.2781212, 46.1949694],
      [15.3251565, 46.2085137],
      [15.328933, 46.2303678],
      [15.3227532, 46.2562489],
      [15.3062737, 46.2695409],
      [15.2602685, 46.2683542]
    ].map(coord => fromLonLat(coord));

    // Create the polygon geometry
    const polygon3 = new Polygon([coordinates3]);

    // Create a feature and set the geometry
    const feature3 = new Feature({
      geometry: polygon3
    });

    const vectorSource3 = new VectorSource({
      features: [feature3]
    });

    // Create a vector layer and add the source
    this.VectorLayerArea3 = new VectorLayer({
      source: vectorSource3,
    });

    const coordinates4 = [
      [15.5387823, 46.6166391],
      [15.5786078, 46.4910374],
      [15.6802313, 46.3016152],
      [15.8683722, 46.3139476],
      [15.9439032, 46.3547197],
      [15.9329168, 46.4673956],
      [15.905451, 46.5798387],
      [15.8189337, 46.6307865],
      [15.5387823, 46.6166391]
    ].map(coord => fromLonLat(coord));

    // Create the polygon geometry
    const polygon4 = new Polygon([coordinates4]);

    // Create a feature and set the geometry
    const feature4 = new Feature({
      geometry: polygon4
    });

    const vectorSource4 = new VectorSource({
      features: [feature4]
    });

    this.VectorLayerArea4 = new VectorLayer({
      source: vectorSource4,
    });

    const coordinates5 = [
      [13.6936245, 45.962868],
      [13.6366329, 45.9638226],
      [13.6263333, 45.9385202],
      [13.6290798, 45.8983945],
      [13.6599789, 45.8859688],
      [13.7155972, 45.8840569],
      [13.7341366, 45.9151171],
      [13.7286434, 45.9504567],
      [13.6936245, 45.962868]
    ].map(coord => fromLonLat(coord));

    // Create the polygon geometry
    const polygon5 = new Polygon([coordinates5]);

    // Create a feature and set the geometry
    const feature5 = new Feature({
      geometry: polygon5
    });

    const vectorSource5 = new VectorSource({
      features: [feature5]
    });

    this.VectorLayerArea5 = new VectorLayer({
      source: vectorSource5,
    });





    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip bg-white text-black  rounded ';
    const overlay = new Overlay({
      element: tooltip,
      offset: [10, 0],
      positioning: 'bottom-center'
    });

    const map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new OSM(),
        }),
        vectorLayer,
        vectorLayer2,
        vectorLayer3,
        this.vectorLayerArea1,
        this.vectorLayerArea2,
        this.VectorLayerArea3,
        this.VectorLayerArea4,
        this.VectorLayerArea5

      ],
      overlays: [overlay],
      view: new View({
        center: fromLonLat([14.995463, 46.151241]), // center on Slovenia
        zoom: 9, // adjust zoom level as needed
      })
    });

    map.on('pointermove', function (event) {
      const feature = map.forEachFeatureAtPixel(event.pixel, function (feature) {
        return feature;
      });

      if (feature) {
        const featureCoordinates = feature.getGeometry().getCoordinates();
        const polygonCoordinates = polygon1.getCoordinates();

        if (JSON.stringify(featureCoordinates) === JSON.stringify(polygonCoordinates)) {
          const coordinate = event.coordinate;
          tooltip.innerHTML = 'Nevarnost poplav: Zelo redke';
          overlay.setPosition(coordinate);
        }
      } else {
        tooltip.innerHTML = '';
        overlay.setPosition(undefined);
      }
    });

    this.fetchData(this.selectedDate);
  },
  created() {
    // Add the map to the DOM
    const today = new Date();
    for (let i = 0; i < 6; i++) {
      const newDate = new Date();
      newDate.setDate(today.getDate() + i);
      this.dates.push(newDate.toISOString().split('T')[0]);
    }
  },

  setup() {
    const store = useStore()

  },

  methods: {
    selectDate(date) {
      this.$store.commit('setSelectedDate', date);
      // ...
    },
    async fetchData(date) {
      try {
        console.log('Fetching data for date:', date);
        // Handle the response data

        this.vectorLayerArea1.setStyle(this.getStyle(1));
        this.vectorLayerArea2.setStyle(this.getStyle(2));
        this.VectorLayerArea3.setStyle(this.getStyle(1));
        this.VectorLayerArea4.setStyle(this.getStyle(1));
        this.VectorLayerArea5.setStyle(this.getStyle(1));

      } catch (error) {
        console.error(error);
      }
    },
    getStyle(number) {
      let color;

      // Assign color based on the input number
      switch (number) {
        case 1:
          color = 'rgba(0, 128, 0, 0.8)'; // Green
          break;
        case 2:
          color = 'rgba(255, 165, 0, 0.8)'; // Orange
          break;
        case 3:
          color = 'rgba(255, 0, 0, 0.8)'; // Red
          break;
        default:
          color = 'rgba(0, 0, 0, 0.8)'; // Default to black
          break;
      }

      return new Style({
        fill: new Fill({
          color: color
        }),
        stroke: new Stroke({
          color: color,
          width: 1
        })
      });
    }
  },

  computed: {
    selectedDate() {
      console.log(this.$store.state.selectedDate);
      return this.$store.state.selectedDate;
    },
  },

  watch: {
    selectedDate(newDate, oldDate) {
      if (newDate !== oldDate) {
        this.fetchData(newDate);
      }
    },
  },

}
</script>

<style scoped>
#map {
  width: 100%;
  height: 70vh;
}
</style>
