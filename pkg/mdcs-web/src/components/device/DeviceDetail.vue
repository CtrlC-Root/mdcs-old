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
        <tr>
          <th scope="row">brightness</th>
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
  data () {
    return {}
  },
  computed: {},
  methods: {}
}
</script>

<style>
</style>
