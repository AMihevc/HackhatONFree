<script setup lang="ts">
import Map from './Map.vue';
import Chat from './Chat.vue';

</script>

<template>
  
  <v-card>
    <v-layout>
      <v-navigation-drawer
        class="bg-deep-purple"
        theme="dark"
        permanent
      >
        <v-list color="transparent">
          <v-list-item prepend-icon="mdi-view-dashboard" title="Zemljevid ogroženosti" @click="selected = Map" ></v-list-item>
          <v-list-item prepend-icon="mdi-account-box" title="Poplavko" @click="selected = Chat"> </v-list-item>
        </v-list>

      </v-navigation-drawer>

      <v-main>
        <component :is="selected" />
      </v-main>

    </v-layout>
  </v-card>
</template>

<script lang="ts">



export default {
  data() {
    return {
      userName: '',
      selected: Map
    };
  },


};
</script>
