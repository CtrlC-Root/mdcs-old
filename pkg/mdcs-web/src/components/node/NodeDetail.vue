<template>
  <div class="container">
    <h3 class="display-3 text-center">Node: {{ node.name }}</h3>

    <!-- Controls -->
    <div class="row">
      <!-- Device Cards -->
      <div class="col-sm-12 col-md-6 col-lg-4 my-2" v-for="device in node.devices">
        <device-card :node="node" :deviceName="device"/>
      </div>
    </div>
  </div>
</template>

<script>
import DeviceCard from './../device/DeviceCard.vue';

export default {
  name: 'node-detail',
  components: {
    'device-card': DeviceCard
  },
  data () {
    return {}
  },
  computed: {
    node () {
      var nodeName = this.$route.params.name;
      return this.$store.state.node.all.find(function (item) {
        return item.name == nodeName;
      });
    }
  },
  methods: {}
}
</script>

<style>
</style>
