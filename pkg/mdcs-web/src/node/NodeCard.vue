<template>
  <div class="card">
    <div class="card-block">
      <h4 class="card-title">hue-bridge</h4>
      <h6 class="card-subtitle mb-2 text-muted">{{ url }}</h6>
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">HTTP API: {{ httpPort }}/tcp</li>
      <li class="list-group-item">TCP API: {{ tcpPort }}/tcp</li>
      <li class="list-group-item">{{ deviceCount }} devices</li>
    </ul>
    <div class="card-footer">
      <button class="btn btn-primary" v-on:click="refresh">Refresh</button>
      <button class="btn btn-danger" v-on:click="disconnect">Disconnect</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'node-card',
  data () {
    return {
      url: '',
      httpPort: NaN,
      tcpPort: NaN,
      deviceCount: 0
    }
  },
  methods: {
    refresh: function () {
      console.log("TODO: refresh node");
    },
    disconnect: function () {
      console.log("TODO: disconnect node");
    }
  }
}
</script>

<style>
</style>
