<template>
  <div class="container">
    <h3 class="display-3 text-center">{{ node.name }}</h3>
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
