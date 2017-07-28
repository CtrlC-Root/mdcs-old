<template>
  <div class="card">
    <div class="card-block">
      <h4 class="card-title">hue-bridge</h4>
      <h6 class="card-subtitle mb-2 text-muted">{{ host }}:{{ httpPort }}</h6>
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">Data: {{ tcpPort }}/tcp</li>
      <li class="list-group-item">{{ deviceCount }} devices</li>
    </ul>
    <div class="card-footer">
      <button class="btn btn-primary">Refresh</button>
      <button class="btn btn-danger">Disconnect</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'node-card',

  data () {
    return {
      'host': '192.168.0.58',
      'httpPort': 5000,
      'tcpPort': 5100,
      'deviceCount': 20
    }
  },

  methods: {}
}
</script>

<style>
</style>
