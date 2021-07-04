<template>
  <q-page class="bg-grey-3 column">
    <div class="row q-pa-sm bg-secondray">
      <q-input
        bg-color="white"
        label="Add Task"
        filled
        class="col"
        v-model="newTask"
        dense
        square
        @keyup.enter="addTask"
      >
        <template v-slot:append>
          <q-btn @click="addTask" round dense flat icon="add" />
        </template>
      </q-input>
    </div>
    <q-list class="bg-white" separator bordered>
      <q-item
        v-for="task in tasks"
        :key="task.id"
        @click="updateTask(task.id, task.done)"
        v-ripple
        :class="{ 'done bg-blue-1 ': task.done }"
        clickable
      >
        <q-item-section avatar>
          <q-checkbox
            v-model="task.done"
            class="no-pointer-events"
            color="primary"
          />
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ task.title }}</q-item-label>
        </q-item-section>
        <q-item-section v-if="task.done">
          <q-item-label>
            <q-btn
              @click.stop="handleOpenDialog(task.id)"
              dense
              flat
              round
              class="float-right"
              color="primary"
              icon="delete"
          /></q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
    <q-dialog v-if="selectedTask" v-model="confirm">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="primary" text-color="white" />
          <span class="q-ml-sm"
            >{{ selectedTask.title }} - Are you sure you wanna delete this</span
          >
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn
            flat
            label="Delete"
            @click="deleteTask(selectedTask.id)"
            color="primary"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <div v-if="!tasks.length" class="no-tasks absolute-center">
      <q-icon name="check" class="q-ml-lg" size="100px" color="primary" />
      <div class="text-h5 text-primary">No Tasks today</div>
    </div>
    <!-- ading alert for connection loss -->
    <q-dialog v-model="alert">
      <q-card>
        <q-card-section>
          <div class="text-h6">Alert</div>
        </q-card-section>

        <q-card-section class="row items-center">
          <q-avatar icon="signal_wifi_off" color="primary" text-color="white" />
          <span class="q-ml-sm"
            >You are currently not connected to any network.</span
          >
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="OK" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { onMounted, ref, computed } from "vue";
import { defineComponent } from "vue";
import { useQuasar } from "quasar";
import { HTTP } from "src/common/api-service.js";

export default defineComponent({
  name: "PageIndex",
  setup() {
    const $q = useQuasar();
    const alert = ref(false);
    const tasks = ref([]);
    const selectedTaskId = ref();
    const confirm = ref(false);
    const handleOpenDialog = function (taskId) {
      confirm.value = true;
      selectedTaskId.value = taskId;
    };
    const selectedTask = computed(() => {
      return tasks.value.find((task) => task.id === selectedTaskId.value);
    });
    onMounted(() => {
      let endpoint = "todo/";
      HTTP.get(endpoint).then((res) => {
        tasks.value.push(...res.data);
      });

      if (navigator.onLine) {
      } else {
        alert.value = true;
      }
    });

    return {
      tasks,
      confirm,
      alert,
      address: ref(""),
      selectedTask,
      handleOpenDialog,
    };
  },
  data() {
    return {
      newTask: "",
    };
  },

  methods: {
    async deleteTask(id) {
      try {
        this.tasks.splice(
          this.tasks.findIndex((task) => task.id === id),
          1
        );
        let endpoint = "todo/" + id + "/";
        await HTTP.delete(endpoint);
      } catch (e) {
        console.log(e);
      }
      this.confirm = false;
      this.$q.notify({
        message: "Task Deleted",
        color: "purple",
      });
    },
    async updateTask(id, donet) {
      if (donet === false) {
        let endpoint = "todo/" + id + "/";
        let res = await HTTP.patch(endpoint, { done: true });
        this.tasks.find((task) => task.id === id).done = true;
      } else {
        let endpoint = "todo/" + id + "/";
        let res = await HTTP.patch(endpoint, { done: false });
        this.tasks.find((task) => task.id === id).done = false;
      }
    },
    async addTask() {
      if (this.newTask) {
        let endpoint = "todo/";
        let res = await HTTP.post(endpoint, { title: this.newTask });
        this.tasks.unshift(res.data);
        this.newTask = "";
      }
    },
  },
});
</script>

<style lang="scss">
.done {
  .q-item__label {
    text-decoration: line-through;
    color: #bbb;
  }
}
.no-tasks {
  opacity: 0.5;
}
</style>
