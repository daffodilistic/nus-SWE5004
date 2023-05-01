<template>
  <q-page class="bg-grey-10">
    <WebSocketComponent class="hidden"></WebSocketComponent>
    <div class="row">
      <div class="col">
        <h3 class="text-white text-center">
          Welcome {{ currentUser.person_name }}!
        </h3>
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
            @click="selectUser(n)"
          >
            <q-avatar size="12em">
              <!-- <img src="https://cdn.quasar.dev/img/avatar.png" /> -->
              <q-icon size="2em" name="account_circle" />
            </q-avatar>
            <h5 class="q-mt-sm q-mb-sm text-center text-black">
              {{ n.person_name }}
            </h5>
          </div>
        </div>
      </q-scroll-area>
    </div>
    <div class="row justify-between">
      <div class="col-auto q-ma-md">
        <q-btn class="" @click="switchUser" color="secondary" label="Switch User" />
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
import { useRouter } from "vue-router";

const currentUser = ref({
  person_name: "John",
});

export default defineComponent({
  name: "DataCollectPage",
  setup() {
    const $router = useRouter();

    onMounted(() => {
      // Set currentUser to data from session storage
      currentUser.value = JSON.parse(sessionStorage.getItem("current_user"));
    });

    return {
      currentUser,
    };
  },
  methods: {
    // register() {
    //   this.$router.push("/register");
    // },
  },
});
</script>
  