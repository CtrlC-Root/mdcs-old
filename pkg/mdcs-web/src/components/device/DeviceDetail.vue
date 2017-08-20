<template>
  <div class="container">
    <h3 class="display-3 text-center">Device: {{ device.name }}</h3>

    <!-- Attributes -->
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Attribute</th>
          <th>Flags</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="attribute in device.attributes">
          <th scope="row" class="w-25">{{ attribute.path }}</th>
          <td class="w-25">{{ attribute.flags.join(', ') }}</td>
          <td class="w-50">
            <div class="input-group">
              <input type="text" class="form-control">
              <span class="input-group-btn">
                <button class="btn btn-primary" type="button">Set</button>
                <button class="btn btn-secondary" type="button"><i class="fa fa-refresh"></i></button>
              </span>
            </div>
          </td>
        </tr>
        <tr v-if="device.attributes.length == 0">
          <td colspan="4">No attributes.</td>
        </tr>
      </tbody>
    </table>

    <!-- TODO: Actions -->
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
