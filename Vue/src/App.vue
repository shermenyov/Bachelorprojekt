/* HTML Template für die Webserverseite: Titel: DEVICE DATA; Inhalt: 'device-items' wird vom Komponent DeviceItems
übernommen; Bereich für das Datei-Hochladen auf der Webseite (handleFileUpload($event)); Buttonbereich 'Submit' für das
Datei-Absenden (submitConfig()) */
<template>
  <div class="container">
    <h1 class="banner">Device data</h1>
    <device-items :devices="devices"></device-items>
    <div class="alerts"></div>
    <button class="refresh-btn btn" @click="getData">Refresh</button>
    <div class="remover" v-if="devices.length">
      <div v-for="device in devices" :key="device.id">
        <button class="remove-btn btn" @click="removeDevice(device.id)">
          <span class="remove-text">Remove</span> {{ device.address }}
        </button>
      </div>
    </div>
    <div class="connect">
      <h2>Connect to Device</h2>
      <input type="url" class="connect_input" placeholder="Device Address" v-model="address" required />
      <input type="text" class="connect_input" placeholder="Login" v-model="login" required />
      <input type="password" class="connect_input" placeholder="Password" v-model="password" required />
      <button class="connect-btn btn" @click="connectToDevice">Get data</button>
    </div>
  </div>
</template>

// Javascript Teil
<script>
import DeviceItems from '@/components/DeviceItems'
import to from 'await-to-js'
import { devicesUrl, connectDeviceUrl, disconnectDeviceUrl } from '@/config/config.json'

export default {
  components: {
    DeviceItems,
  },
  data() {
    return {
      address: '',
      login: '',
      password: '',
      devices: [],
    }
  },

  methods: {
    async getData() {
      const [devicesDataRequestError, devicesDataRequest] = await to(
        fetch(devicesUrl, {
          method: 'GET',
          // method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
        })
      )

      console.log(devicesUrl, 'devicesDataRequestError', devicesDataRequestError)
      console.log(devicesUrl, 'devicesDataRequest', devicesDataRequest)

      const [devicesDataError, devicesData] = await to(devicesDataRequest.json())

      console.log(devicesUrl, 'devicesDataError', devicesDataError)
      console.log(devicesUrl, 'devicesData', devicesData)

      if (devicesDataError || !devicesData) {
        return null
      }

      // const newDevices = Object.values(devicesData).splice(0, 3)
      const newDevices = devicesData

      this.devices = newDevices
    },
    async connectToDevice() {
      const [deviceLoginRequestError, deviceLoginRequest] = await to(
        fetch(connectDeviceUrl, {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            address: this.address,
            login: this.login,
            password: this.password,
          }),
        })
      )

      console.log(connectDeviceUrl, 'deviceLoginRequestError', deviceLoginRequestError)
      console.log(connectDeviceUrl, 'deviceLoginRequest', deviceLoginRequest)

      this.getData()

      this.address = ''
      this.login = ''
      this.password = ''
    },
    async removeDevice(id) {
      console.log(id)
      const [deviceRemoveRequestError, deviceRemoveRequest] = await to(
        fetch(disconnectDeviceUrl, {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: id,
          }),
        })
      )

      console.log(disconnectDeviceUrl, 'deviceRemoveRequestError', deviceRemoveRequestError)
      console.log(disconnectDeviceUrl, 'deviceRemoveRequest', deviceRemoveRequest)

      this.getData()
    },
  },
  // Übernehmen von Daten aus dem Flask-Server werden durch die Funktion mounted()
  // nach dem Aufbau der Webseite ausgeführt
  mounted() {
    this.getData()
  },
}
</script>

// CSS Styles von Tailwind
<style scoped>
.container {
  background: #f4f3f3;
  margin: 0 auto;
  padding: 20px;
  box-shadow: 0 0 5px rgb(0 0 0 / 20%);
  margin-top: 20px;
}

.banner {
  text-transform: uppercase;
  text-align: center;
  font-size: 40px;
  color: #9aa080;
  letter-spacing: 1px;
}

.btn {
  border: 1px solid grey;
  padding: 5px 20px;
  margin: 10px 10px 10px 0;
}

.refresh-btn {
  width: 200px;
  background-color: #a1a1a1;
  color: #000;
  transition: background 0.2s ease;
}
.refresh-btn:hover {
  background-color: #cfcfcf;
}

.connect {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
}

.connect h2 {
  font-size: 24px;
}

.connect_input {
  padding: 5px 10px;
  margin: 10px 0;
  width: 300px;
}

.connect-btn {
  width: 200px;
  background-color: #a1a1a1;
  color: #000;
  transition: background 0.2s ease;
}
.connect-btn:hover {
  background-color: #cfcfcf;
}

.remove-btn {
  transition: background 0.2s ease;
}

.remove-btn:hover {
  background-color: rgb(221, 157, 157);
}

.remove-text {
  color: red;
}
</style>
