<template>
  <div>
    <h6>WebSocket Component</h6>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: 'WebSocketComponent',
  setup() {
    console.log("WebSocket component loaded");

    const eventsFromServer = ref([
      // { data: 'hii', time: '32234' },
      // { data: 'hii324', time: '3223422' },
    ]);
    const serverUrl =
      process.env.NODE_ENV === "production"
        ? "YOUR_WEBSOCKET_URL"
        : "ws://localhost:8000/events";
    let familyMembers = ref([]);

    const socket = new WebSocket(serverUrl);
    socket.addEventListener("open", (event) => {
      console.log("Connected to server");
    });

    socket.addEventListener("message", function (event) {
      console.log("Message from server ", event.data);
      eventsFromServer.value.push({ time: new Date(), data: event.data });
    });

    return {
      eventsFromServer,
    };
  },
})
</script>
