<template>
  <div class="container">
    <h3 class="display-3 text-center">Device: {{ device.name }}</h3>

    <table class="table table-striped">
      <thead>
        <tr>
          <th>Attribute</th>
          <th>Flags</th>
          <th>Schema</th>
          <th>Controls</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="attribute in device.attributes">
          <th scope="row">{{ attribute.path }}</th>
          <td>{{ attribute.flags.join(', ') }}</td>
          <td>{{ attribute.schema }}</td>
          <td>TODO</td>
        </tr>
        <tr v-if="device.attributes.length == 0">
          <td colspan="4">No attributes.</td>
        </tr>
      </tbody>
    </table>

    <table class="table table-striped">
      <thead>
        <tr>
          <th>Action</th>
          <th>Input Schema</th>
          <th>Output Schema</th>
          <th>Controls</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="action in device.actions">
          <th scope="row">{{ action.path }}</th>
          <td>{{ action.inputSchema }}</td>
          <td>{{ action.outputSchema }}</td>
          <td>TODO</td>
        </tr>
        <tr v-if="device.actions.length == 0">
          <td colspan="4">No actions.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'device-detail',
  data () {
    return {};
  },
  computed: {
    node () {
      var nodeName = this.$route.params.node;
      return this.$store.state.node.all.find(function (item) {
        return item.name == nodeName;
      });
    },
    device () {
      var deviceName = this.$route.params.device;
      return this.node.devices.find(function (device) {
        return device.name == deviceName;
      });
    }
  }
}
</script>

<style>
</style>
