<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">
        <router-link :to="{name: 'device-detail', params: {node: node.name, device: device.name}}">
          {{ title }}
        </router-link>
      </h4>
      <h6 class="card-subtitle mb-2 text-muted" v-if="title != device.name">{{ device.name }}</h6>
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">{{ device.attributes.length }} attributes</li>
      <li class="list-group-item">{{ device.actions.length }} actions</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'device-card',
  props: ['node', 'device'],
  created () {
    this.loadName();
  },
  data () {
    return {
      'title': this.device.name
    };
  },
  methods: {
    loadName () {
      // check if the device has a name attribute
      var attribute = this.device.attributes.find((attribute) => {
        return attribute.path == 'name';
      });

      if (attribute) {
        // retrieve the name attribute value
        var nodeUrl = `http://${this.node.host}:${this.node.httpPort}`;
        return this.$http.get(`${nodeUrl}/d/${this.device.name}/at/name/v`).then((response) => {
          // override the title
          this.title = response.body;
        });
      }
    }
  }
}
</script>
