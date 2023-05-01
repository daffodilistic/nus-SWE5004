<template>
  <div>
    <h6>WebSocket Component</h6>
  </div>
</template>

<script>
import { defineComponent, defineEmits, ref } from "vue";

export default defineComponent({
  name: "WebSocketComponent",
  setup(props, context) {
    console.log("WebSocket component loaded");
    // const emits = defineEmits(["wss_message"]);
    const eventsFromServer = ref([]);
    // const serverUrl =
    //   process.env.NODE_ENV === "production"
    //     ? "ws://localhost:8000/events"
    //     : "wss://emulator.mariotoilet.xyz/events";
    const serverUrl = "wss://emulator.mariotoilet.xyz/events";

    const socket = new WebSocket(serverUrl);
    socket.addEventListener("open", (event) => {
      console.log("Connected to server");
    });

    socket.addEventListener("message", (event) => {
      console.log("Message from server ", event.data);
      context.emit('onWebSocketMessage', event.data);
      eventsFromServer.value.push({ time: new Date(), data: event.data });
    });

    return {
      eventsFromServer,
    };
  },
});
</script>
