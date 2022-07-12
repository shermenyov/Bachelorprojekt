/* HTML Template erstellt einen Bereich für jedes Device als eine zweispaltige Tabelle. Die Tabellendaten auf der
rechten Seite werden vom Objekt'device'(@/components/DeviceItems) abgelesen*/
<template>
  <tr>
    <td>{{ device.address }}</td>
    <td>{{ device.softwareVersion }}</td>
    <td>{{ device.boardTemperature }}</td>
    <td>{{ device.speakerVolume }}</td>
    <td>{{ device.microphoneVolume }}</td>
    <td>{{ device.ringToneVolume }}</td>
    <td>{{ device.announcementVolume }}</td>
  </tr>
</template>

<script>
export default {
  props: {
    device: {
      type: Object,
    },
  },
}
</script>

<style scoped>
td {
  padding: 0 10px;
  border: 1px solid grey;
  white-space: normal;
  word-break: break-all;
  word-wrap: break-word;
  width: auto;
}
</style>
