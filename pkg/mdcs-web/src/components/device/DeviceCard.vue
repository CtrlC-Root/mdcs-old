<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">
        <router-link :to="{name: 'device-detail', params: {node: node.name, device: device.name}}">
          {{ device.name }}
        </router-link>
      </h4>
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
  data () {
    return {};
  }
}
</script>
