<template>
  <div class="container">
    <h3 class="display-3 text-center">Network</h3>

    <!-- Controls -->
    <div class="row">
      <!-- Node Cards -->
      <div class="col-sm-12 col-md-6 col-lg-4 my-2">
        <node-card />
      </div>

      <div class="col-sm-12 col-md-6 col-lg-4 my-2">
        <node-card />
      </div>

      <!-- Connect to Node Card -->
      <div class="col-sm-12 col-md-6 col-lg-4 my-2">
        <div class="card card-template">
          <div class="card-block">
            <form>
              <div class="form-group">
                <input type="text" class="form-control" id="nodeHost" placeholder="Hostname or IP address">
              </div>
              <div class="form-group">
                <input type="text" class="form-control" id="nodeHttpPort" placeholder="HTTP API port">
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
    return {}
  },
  methods: {}
}
</script>

<style>
</style>
