<template>
  <div>
    <div v-for="(msg, index) in conversationHistory" :key="index" >
      <p><strong>{{ msg.role }}:</strong> {{ msg.content }}</p>
    </div>

    <form @submit.prevent="sendMessage">
      <input v-model="userMessage" type="text" placeholder="Type your message here...">
      <button type="submit">Send</button>
    </form>
  </div>
</template>

<script>

import OpenAI from "openai";
export default {

  methods: {
    // methods
  },
  computed: {
    // computed properties
    selectedDate() {
      console.log(this.$store.state.selectedDate);
      return this.$store.state.selectedDate;
    },
  },

  data() {
    return {
      conversationHistory: [
        { "role": "system", "content": "You are an expert on floods. You have data for a city where the chance of a flood is high. You are asked", "show": false },
        { "role": "user", "content": "Is there going to be flood?", "show": false },
        { "role": "assistant", "content": "Based on the data available for the city with a high risk of flooding, we can say that there is a high probability of a flood occurring. However, it is not possible to predict with certainty whether a flood will definitely happen or not. It is important to stay informed about weather forecasts and follow the guidance provided by local authorities to stay safe in case of a flood.", "show": false },
        // Continue adding messages as the conversation progresses
      ],
      userMessage: ''
    };
  },
  methods: {
    async sendMessage() {
      // Add the user's message to the conversation history
      this.conversationHistory.push({ role: 'user', content: this.userMessage, show: true });
      console.log(this.conversationHistory);

      // Send the message to the OpenAI API and get the response
      const openai = new OpenAI({ apiKey: 'sk-proj-bzgRr2hFwrCnGFZX1VsWT3BlbkFJhF8GoNVWH2T5aWBdOdEn', dangerouslyAllowBrowser: true });
      const completion = await openai.chat.completions.create({
        messages: this.conversationHistory,
        model: "gpt-3.5-turbo",
      });

      // Add the assistant's response to the conversation history
      this.conversationHistory.push({ role: 'assistant', content: completion.choices[0].message.content, show: true });

      // Clear the user's message
      this.userMessage = '';
    }
  },

  mounted() {
    console.log('Initial conversationHistory:', this.conversationHistory);
  },
  watch: {
    conversationHistory(newVal) {
      console.log('Updated conversationHistory:', newVal);
    },
  },

  // etc.
}
</script>