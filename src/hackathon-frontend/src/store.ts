import { createStore } from 'vuex';


export default createStore({
  state: {
    selectedDate: new Date().toISOString().split('T')[0],
  },
  mutations: {
    setSelectedDate(state, date) {
      state.selectedDate = date;
    },
  },

});