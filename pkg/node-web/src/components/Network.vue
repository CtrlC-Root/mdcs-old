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
          <div class="card-body">
            <h4 class="card-title">
              Add Node
              <i class="fa fa-refresh fa-spin" v-if="loading"></i>
            </h4>
            <form v-on:submit.prevent="connectNode">
              <div class="form-group">
                <label class="form-control-label" for="nodeUrl">HTTP API URL</label>
                <input type="text"
                  class="form-control"
                  id="nodeUrl"
                  placeholder="http://127.0.0.1:5510/"
                  v-bind:class="{'is-invalid': error}"
                  v-model="nodeUrl">
                <div class="invalid-feedback" v-if="error">{{ error }}</div>
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
import NodeCard from './node/NodeCard.vue';

export default {
  name: 'network',
  components: {
    'node-card': NodeCard
  },
  data () {
    return {
      nodeUrl: '',
      error: '',
      loading: false
    }
  },
  computed: {
    nodes () {
      return this.$store.state.node.all;
    }
  },
  methods: {
    connectNode: function () {
      this.loading = true;
      this.$store.dispatch('connectNode', {
        nodeUrl: this.nodeUrl
      }).then((node) => {
        this.error = '';
        this.nodeUrl = '';
      }, (error) => {
        this.error = 'Failed to connect!';
      }).then(() => {
        this.loading = false;
      });
    }
  }
}
</script>
