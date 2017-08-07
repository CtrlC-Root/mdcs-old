<template>
  <div class="container">
    <h3 class="display-3 text-center">Device: TODO</h3>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Attribute</th>
          <th>Flags</th>
          <th>Schema</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="attribute in attributes">
          <th scope="row">{{ attribute }}</th>
          <td>READ, WRITE</td>
          <td>{'type': 'integer'}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'device-detail',
  created () {
    this.refresh();
  },
  data () {
    return {
      'error': false,
      'loading': true,
      'attributes': [],
      'actions': []
    };
  },
  computed: {
    node () {
      var nodeName = this.$route.params.node;
      return this.$store.state.node.all.find(function (item) {
        return item.name == nodeName;
      });
    },
    deviceName () {
      return this.$route.params.device;
    }
  },
  methods: {
    refresh () {
      this.loading = true;
      this.$http.get(`http://${this.node.host}:${this.node.httpPort}/d/${this.deviceName}`).then((response) => {
        return response.json();
      }).then((data) => {
        this.attributes = data.attributes;
        this.actions = data.actions;
        this.error = false;
      }).catch((response) => {
        this.attributs = [];
        this.actions = [];
        this.error = true;
      }).then(() => {
        this.loading = false;
      });
    }
  }
}
</script>

<style>
</style>
