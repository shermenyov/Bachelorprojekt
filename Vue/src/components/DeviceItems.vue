/* HTML Template übernimmt das Muster-Template vom Komponent 'DeviceItem' und verbreitet das für alle 3 Devices*/
<template>
  <div class="container" v-if="devices.length">
    <table>
      <tr>
        <th>Name</th>
        <th>Software Version</th>
        <th>Board Temperature</th>
        <th>Speaker Volume</th>
        <th>Microphone Volume</th>
        <th>RingTone Volume</th>
        <th>Announcement Volume</th>
      </tr>
      <device-item :device="device" v-for="device in devices" :key="device.id"></device-item>
    </table>
  </div>
  <p v-else>No devices connected</p>
</template>

<script>
import DeviceItem from '@/components/DeviceItem'

export default {
  components: {
    DeviceItem,
  },
  props: {
    devices: {
      type: Array,
    },
  },
}
</script>

<style scoped>
.container {
  display: flex;
}
table {
  table-layout: fixed;
  width: 100%;
}
th {
  padding: 0 10px;
  border: 2px solid grey;
}
</style>
