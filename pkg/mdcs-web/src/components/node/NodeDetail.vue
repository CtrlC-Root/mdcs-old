<template>
  <div class="container">
    <h3 class="display-3 text-center">Node: {{ node.host }}</h3>
    <ul>
      <li v-for="device in node.devices">{{ device }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'node-detail',
  data () {
    return {}
  },
  computed: {
    node () {
      var nodeId = parseInt(this.$route.params.id);
      return this.$store.state.node.all.find(function (item) {
        return item.id == nodeId;
      });
    }
  },
  methods: {}
}
</script>

<style>
</style>
