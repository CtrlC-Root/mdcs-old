<template>
  <div class="card">
    <div class="card-block">
      <h4 class="card-title">
        <router-link :to="{name: 'node-detail', params: {node: node.name}}">{{ node.name }}</router-link>
        <i class="fa fa-refresh fa-spin" v-if="node.loading"></i>
      </h4>
      <h6 class="card-subtitle mb-2 text-muted">{{ node.host }}</h6>
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">HTTP API: {{ node.httpPort }}/tcp</li>
      <li class="list-group-item">TCP API: {{ node.tcpPort }}/tcp</li>
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
  props: ['node'],
  data () {
    return {};
  },
  computed: {
    deviceCount: function () {
      return this.node.devices.length
    }
  },
  methods: {
    refresh: function () {
      this.$store.dispatch('refreshNode', this.node);
    },
    disconnect: function () {
      this.$store.commit('removeNode', this.node);
    }
  }
}
</script>
