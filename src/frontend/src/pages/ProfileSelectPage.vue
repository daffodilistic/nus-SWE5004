<template>
  <q-page class="bg-blue-grey">
    <div class="row">
      <div class="col">
        <h3 class="text-white text-center">Welcome! Select a User Profile</h3>
      </div>
    </div>
    <div class="row">
      <q-scroll-area style="min-height: 18em; min-width: 100vw">
        <div class="row no-wrap items-center justify-center">
          <div
            v-for="n in familyMembers"
            :key="n"
            style="height: auto; width: auto"
            class="q-ma-sm q-pa-sm bg-amber-2 items-center justify-center shadow-4"
          >

            <q-avatar size="12em">
              <!-- <img src="https://cdn.quasar.dev/img/avatar.png" /> -->
              <q-icon size="2em" name="account_circle" />
            </q-avatar>
            <h5 class="q-mt-sm q-mb-sm text-center text-black">{{n.person_name}}</h5>
          </div>
        </div>
      </q-scroll-area>
    </div>
    <div class="row justify-between">
      <div class="col-auto q-ma-md">
        <q-btn class="" @click="addUser" color="primary" label="Add User" />
      </div>
      <div class="col-auto q-ma-md">
        <q-btn class="" @click="logout" color="negative" label="Logout" />
      </div>
    </div>
    <q-dialog v-model="showAddUserDialog" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Enter user name</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            dense
            v-model="newUserName"
            autofocus
            @keyup.enter="showAddUserDialog = false"
          />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn flat label="Add User" :loading="loading" @click="addNewUser" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style lang="sass" scoped>
.user-profile
  width: 100%
  height: 100%
  max-height: 250px
  max-width: 250px
</style>

<script>
import { defineComponent, onMounted, ref } from "vue";
import { api } from "boot/axios";

export default defineComponent({
  name: "ProfileSelectPage",
  setup() {
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

    onMounted(() => {
      // Get family members from session storage
      const accountUsers = JSON.parse(sessionStorage.getItem("family_members"));
      // console.log(accountUsers);
      if (accountUsers) {
        familyMembers.value = accountUsers;
      }
    });

    return {
      showAddUserDialog: ref(false),
      loading: ref(false),
      newUserName: ref(""),
      familyMembers,
      eventsFromServer,
    };
  },
  methods: {
    logout() {
      sessionStorage.clear();
      this.$router.replace("/");
    },
    addUser() {
      this.showAddUserDialog = true;
    },
    async addNewUser() {
      this.loading = true;
      // this.showAddUserDialog = false;
      const accountData = JSON.parse(sessionStorage.getItem("account"));
      // console.log(accountData);
      const payload = {
          "accountId" : accountData.id,
          "personName" : this.newUserName
      }
      // console.log(payload);
      const response = await api.post("/users", payload);
      console.log("New user data is", response.data);
      if (response.data) {
        this.familyMembers.push(response.data);
        sessionStorage.setItem("family_members", JSON.stringify(this.familyMembers));
        this.showAddUserDialog = false;
      }
    },
  },
});
</script>
