<template>
  <q-page class="bg-grey-10">
    <WebSocketComponent class="hidden"></WebSocketComponent>
    <div class="row">
      <div class="col">
        <h3 class="text-white text-center">
          Welcome {{ currentUser.person_name }}!
        </h3>
        <h6 class="text-white text-center q-mb-sm">Please select an option</h6>
      </div>
    </div>
    <div class="row">
      <div class="col column items-center">
        <div class="col">
          <q-btn
            @click="keyInDiet"
            color="primary"
            label="Key In Today's Diet"
          ></q-btn>
        </div>
        <q-space class="q-my-sm" />
        <div class="col">
          <q-btn
            @click="analyzeMyData"
            color="secondary"
            label="Analyze My Data"
          ></q-btn>
        </div>
        <q-space class="q-my-sm" />
        <div class="col">
          <q-btn color="info" label="View Past Data"></q-btn>
        </div>
        <q-space class="q-my-lg" />
        <div class="col">
          <q-btn
            class=""
            @click="switchUser"
            color="negative"
            label="Switch User"
          />
        </div>
      </div>
    </div>
    <q-dialog v-model="showDietDialog" persistent>
      <q-card style="min-width: 32em; min-height: 14em">
        <q-card-section>
          <div class="text-h6">Key in Today's Diet</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-select
            filled
            v-model="dietForToday"
            multiple
            :options="getDietList"
            use-chips
            stack-label
            label="Select your foods taken for today"
          />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn flat label="Confirm" :loading="loading" @click="confirmDiet" />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="showRecommendedDietDialog" persistent>
      <q-card style="min-width: 32em; min-height: 14em">
        <q-card-section>
          <div class="text-h6">Your Recommended Diet</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <p class="">
            Your urine is acidic. We recommend you to have more of the following
            foods in your diet to balance your pH level.
          </p>
          <p class="text-bold">{{ recommendedDiet }}</p>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Close" v-close-popup />
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
import WebSocketComponent from "src/components/WebSocketComponent.vue";
import dietList from "src/libs/dietList.js";
import { api, apiML } from "boot/axios";
import QSpinnerGears from "quasar/src/components/spinner/QSpinnerGears.js";

const currentUser = ref({
  person_name: "Wu Ming Zhi (无名子)",
});
const recommendedDiet = ref("Chicken, Cake, Banana");

export default defineComponent({
  name: "DataCollectPage",
  setup() {
    // const $router = useRouter();
    const showDietDialog = ref(false);
    const showRecommendedDietDialog = ref(false);
    const dietForToday = ref([]);
    const getDietList = ref(Object.keys(dietList));
    const loading = ref(false);
    // const getDietList = () => {
    //   console.log(Object.keys(dietList));
    //   return Object.keys(dietList);
    // };

    onMounted(() => {
      // Set currentUser to data from session storage
      currentUser.value = JSON.parse(sessionStorage.getItem("current_user"));
    });

    return {
      currentUser,
      showDietDialog,
      showRecommendedDietDialog,
      recommendedDiet,
      dietForToday,
      getDietList,
      loading,
    };
  },
  methods: {
    switchUser() {
      sessionStorage.removeItem("current_user");
      this.$router.push("/profiles");
    },
    keyInDiet() {
      this.showDietDialog = true;
    },
    async confirmDiet() {
      this.loading = true;

      // Pack data to send to backend
      const payload = {
        person_id: this.currentUser.person_id,
      };

      this.getDietList.forEach((key) => {
        if (this.dietForToday.indexOf(key) > -1) {
          payload[key] = 1;
        } else {
          payload[key] = 0;
        }
      });

      // console.log(payload);

      try {
        // Insert dietary data to database
        const response = await apiML.post("/insertDiet", payload);
        // console.log(response);

        this.showDietDialog = false;
        this.dietForToday = [];
        this.$q.notify({
          group: false,
          color: "positive",
          message: "Diet for today has been recorded!",
          timeout: 5000,
        });

        const spinnerHandle = this.$q.notify({
          group: false,
          spinner: QSpinnerGears,
          message: "Working...",
          timeout: 0,
        });

        // Get predicted pH value
        const dietData = payload;
        delete dietData.person_id;
        const mlResponse = await apiML.post("/predictph", dietData);
        console.log(mlResponse.data);

        // Get recommended diet
        const predictedPh = mlResponse.data.body.predicted_urine;
        console.log("Predicted pH is ", predictedPh);
        const dietResponse = await apiML.post(
          "/getRecommendedDiet",
          predictedPh
        );
        console.log(dietResponse.data);
        this.recommendedDiet =
          dietResponse.data.body.recommended_items.join(", ");

        this.loading = false;
        spinnerHandle({
          timeout: 1,
        });
        this.showRecommendedDietDialog = true;
      } catch (error) {
        console.log(error);
        if (error.response.status === 401) {
          this.$q.notify({
            color: "negative",
            message: "Error in recording diet for today!",
          });
        } else {
          this.$q.notify({
            color: "negative",
            position: "top",
            message: "Loading failed",
            icon: "report_problem",
          });
        }
      }
    },
    async analyzeMyData() {
      // TODO need to call https://19k36m49u9.execute-api.us-east-1.amazonaws.com/prod/updateurineph
      //this.loading = true;
      this.$q.notify({
        message: "Waiting for device...",
        type: "warning",
        spinner: true,
        timeout: 0,
        actions: [
          {
            label: "Cancel",
            color: "red",
            handler: () => {
              /* ... */
            },
          },
        ],
      });
    },
  },
  components: {
    WebSocketComponent,
  },
});
</script>
  