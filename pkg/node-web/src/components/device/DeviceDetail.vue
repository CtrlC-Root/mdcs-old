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
            <boolean-field :node="node" :device="device" :attribute="attribute" v-if="attribute.schema == 'boolean'"/>
            <integer-field :node="node" :device="device" :attribute="attribute" v-if="attribute.schema == 'int'"/>
            <string-field :node="node" :device="device" :attribute="attribute" v-if="attribute.schema == 'string'"/>
            <enum-field :node="node" :device="device" :attribute="attribute" v-if="attribute.schema.type == 'enum'"/>
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
import BooleanField from './../input/BooleanField.vue';
import IntegerField from './../input/IntegerField.vue';
import StringField from './../input/StringField.vue';
import EnumField from './../input/EnumField.vue';

export default {
  name: 'device-detail',
  components: {
    'boolean-field': BooleanField,
    'integer-field': IntegerField,
    'string-field': StringField,
    'enum-field': EnumField
  },
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
