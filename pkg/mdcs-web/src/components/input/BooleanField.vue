<template>
  <div>
    <div class="btn-group">
      <label class="btn" v-bind:class="{'btn-primary': value == 'on', 'btn-secondary': value == 'off'}">
        <input type="radio" v-bind:id="attribute.path" value="on" autocomplete="off" v-model="value"> On
      </label>
      <label class="btn" v-bind:class="{'btn-danger': value == 'off', 'btn-secondary': value == 'on'}">
        <input type="radio" v-bind:id="attribute.path" value="off" autocomplete="off" v-model="value"> Off
      </label>
    </div>
    <i class="fa fa-refresh fa-spin" v-if="loading"></i>
  </div>
</template>

<script>
export default {
  name: 'boolean-field',
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
  watch: {
    value: function () {
      this.write();
    }
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
        if (response.body) {
          this.value = 'on';
        }
        else {
          this.value = 'off';
        }
      }).catch((response) => {
        this.error = 'Failed to read value!';
      }).then(() => {
        this.loading = false;
      });
    },
    write () {
      this.loading = true;
      return this.$http.put(this.valueUrl, this.value == 'on').then((response) => {
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
