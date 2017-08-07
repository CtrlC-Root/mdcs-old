<template>
  <div class="card">
    <div class="card-block">
      <h4 class="card-title">
        <router-link :to="{name: 'device-detail', params: {node: node.name, device: deviceName}}">
          {{ deviceName }}
        </router-link>
        <i class="fa fa-refresh fa-spin" v-if="loading"></i>
        <i class="fa fa-exclamation-triangle" v-if="error"></i>
      </h4>
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">{{ attributeCount }} attributes</li>
      <li class="list-group-item">{{ actionCount }} actions</li>
    </ul>
    <div class="card-footer">
      <button class="btn btn-primary" v-on:click="refresh">Refresh</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'device-card',
  props: ['node', 'deviceName'],
  created () {
    this.refresh();
  },
  data () {
    return {
      error: false,
      loading: false,
      attributeCount: NaN,
      actionCount: NaN
    };
  },
  methods: {
    refresh: function () {
      this.loading = true;
      this.$http.get(`http://${this.node.host}:${this.node.httpPort}/d/${this.deviceName}`).then((response) => {
        return response.json();
      }).then((data) => {
        this.attributeCount = data.attributes.length;
        this.actionCount = data.actions.length;
        this.error = false;
      }).catch((response) => {
        this.attributeCount = NaN;
        this.actionCount = NaN;
        this.error = true;
      }).then(() => {
        this.loading = false;
      });
    }
  }
}
</script>
