<template>
  <div class="container">
    <h3 class="display-3 text-center">Network</h3>

    <!-- Controls -->
    <div class="row">
      <!-- Node Cards -->
      <div class="col-sm-12 col-md-6 col-lg-4 my-2" v-for="node in nodes">
        <node-card :node="node"/>
      </div>

      <!-- Connect to Node Card -->
      <div class="col-sm-12 col-md-6 col-lg-4 my-2">
        <div class="card card-template">
          <div class="card-block">
            <h4 class="card-title">Add Node</h4>
            <form v-on:submit.prevent="connectNode">
              <div class="form-group">
                <label for="nodeUrl">HTTP API URL</label>
                <input type="text"
                  class="form-control"
                  id="nodeUrl"
                  placeholder="http://127.0.0.1:5510/"
                  v-model="nodeUrl">
              </div>
              <div class="form-group">
                <input type="submit" class="btn btn-primary" value="Connect">
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NodeCard from './node/NodeCard.vue'

export default {
  name: 'network',
  components: {
    'node-card': NodeCard
  },
  data () {
    return {
      'nodeUrl': ''
    }
  },
  computed: {
    nodes () {
      return this.$store.state.nodes;
    }
  },
  methods: {
    connectNode: function () {
      console.log("TODO: connect to new node: " + this.nodeUrl);
      this.$store.commit('addNode', {
        host: '127.0.0.1',
        httpPort: 5510,
        tcpPort: 5511,
        devices: []
      });

      this.nodeUrl = '';
    }
  }
}
</script>

<style>
</style>
