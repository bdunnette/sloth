<template>
  <div class="attendance-dashboard container mt-4">
    <header class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="display-4 text-primary">Live Attendance</h1>
      <div class="date-display lead">{{ currentDate }}</div>
    </header>

    <div class="row">
      <!-- Coaches Section -->
      <div class="col-md-6 mb-4">
        <div class="card shadow-sm border-0">
          <div
            class="card-header bg-dark text-white d-flex justify-content-between align-items-center"
          >
            <h2 class="h5 mb-0">Coaches</h2>
            <span class="badge bg-light text-dark">{{
              coachesInAttendance.length
            }}</span>
          </div>
          <div class="card-body p-0">
            <ul class="list-group list-group-flush">
              <li
                v-if="coachesInAttendance.length === 0"
                class="list-group-item text-muted text-center py-4"
              >
                No coaches checked in.
              </li>
              <li
                v-for="entry in coachesInAttendance"
                :key="entry.id"
                class="list-group-item d-flex justify-content-between align-items-center py-3"
              >
                <div>
                  <strong class="text-dark">{{
                    entry.derby_name || entry.person_name
                  }}</strong>
                  <div class="small text-muted" v-if="entry.derby_name">
                    {{ entry.person_name }}
                  </div>
                </div>
                <span class="badge bg-success rounded-pill">Present</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Skaters Section -->
      <div class="col-md-6 mb-4">
        <div class="card shadow-sm border-0">
          <div
            class="card-header bg-primary text-white d-flex justify-content-between align-items-center"
          >
            <h2 class="h5 mb-0">Skaters</h2>
            <span class="badge bg-light text-dark">{{
              skatersInAttendance.length
            }}</span>
          </div>
          <div class="card-body p-0">
            <ul class="list-group list-group-flush">
              <li
                v-if="skatersInAttendance.length === 0"
                class="list-group-item text-muted text-center py-4"
              >
                No skaters checked in.
              </li>
              <li
                v-for="entry in skatersInAttendance"
                :key="entry.id"
                class="list-group-item d-flex justify-content-between align-items-center py-3"
              >
                <div>
                  <strong class="text-dark">{{
                    entry.derby_name || entry.person_name
                  }}</strong>
                  <div class="small text-muted" v-if="entry.derby_name">
                    {{ entry.person_name }}
                  </div>
                </div>
                <span v-if="entry.paid_dues" class="badge bg-info me-2"
                  >Dues Paid</span
                >
                <span class="badge bg-success rounded-pill">Present</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center mt-4">
      <button
        @click="fetchAttendance"
        class="btn btn-outline-secondary btn-sm"
        :disabled="loading"
      >
        <span
          v-if="loading"
          class="spinner-border spinner-border-sm me-1"
          role="status"
          aria-hidden="true"
        ></span>
        Refresh Data
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';

export default {
  name: 'AttendanceDashboard',
  setup() {
    const attendanceRecords = ref([]);
    const loading = ref(false);
    const currentDate = new Date().toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });

    const fetchAttendance = async () => {
      loading.value = true;
      try {
        const response = await fetch('/api/attendance/?today=true');
        const data = await response.json();
        attendanceRecords.value = data;
      } catch (error) {
        console.error('Error fetching attendance:', error);
      } finally {
        loading.value = false;
      }
    };

    const coachesInAttendance = computed(() => {
      return attendanceRecords.value.filter(
        (record) => record.person_type === 'coach',
      );
    });

    const skatersInAttendance = computed(() => {
      return attendanceRecords.value.filter(
        (record) => record.person_type === 'skater',
      );
    });

    onMounted(() => {
      fetchAttendance();
      // Auto-refresh every 30 seconds
      setInterval(fetchAttendance, 30000);
    });

    return {
      attendanceRecords,
      loading,
      currentDate,
      coachesInAttendance,
      skatersInAttendance,
      fetchAttendance,
    };
  },
};
</script>

<style scoped>
.attendance-dashboard {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.list-group-item {
  border-left: 4px solid transparent;
  transition: all 0.2s;
}

.list-group-item:hover {
  background-color: #f8f9fa;
  border-left: 4px solid #0d6efd;
}
</style>
