<template>
  <div class="input-group">
    <input type="text"
      class="form-control"
      v-model="value"
      v-bind:class="{'is-invalid': error}"
      v-bind:readonly="!writable || loading">

    <span class="input-group-btn">
      <button class="btn btn-primary" type="button" v-bind:disabled="!writable || loading" v-on:click="write">
        Set
      </button>
      <button class="btn btn-info" type="button" v-bind:disabled="!readable || loading" v-on:click="read">
        <i class="fa fa-refresh" v-bind:class="{'fa-spin': loading}"></i>
      </button>
    </span>
  </div>
</template>

<script>
export default {
  name: 'string-field',
  props: ['node', 'device', 'attribute'],
  created () {
    this.read();
  },
  data () {
    return {
      'loading': false,
      'error': '',
      'value': ''
    };
  },
  computed: {
    valueUrl () {
      return `http://${this.node.host}:${this.node.httpPort}/d/${this.device.name}/at/${this.attribute.path}/v`;
    },
    readable () {
      return this.attribute.flags.includes('READ');
    },
    writable () {
      return this.attribute.flags.includes('WRITE');
    }
  },
  methods: {
    read () {
      this.loading = true;
      return this.$http.get(this.valueUrl).then((response) => {
        this.error = '';
        this.value = response.body;
      }).catch((response) => {
        this.error = 'Failed to read value!';
      }).then(() => {
        this.loading = false;
      });
    },
    write () {
      this.loading = true;
      return this.$http.put(this.valueUrl, JSON.stringify(this.value)).then((response) => {
        this.error = '';
      }).catch((response) => {
        this.error = 'Failed to write value!';
      }).then(() => {
        this.loading = false;
      });
    }
  }
}
</script>
