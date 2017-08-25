<template>
  <div>
    <div class="btn-group" role="group">
      <button
        type="button"
        class="btn"
        v-bind:class="{'btn-primary': value == 'on', 'btn-secondary': value == 'off'}"
        v-on:click="turnOn">
        On
      </button>
      <button
        type="button"
        class="btn"
        v-bind:class="{'btn-danger': value == 'off', 'btn-secondary': value == 'on'}"
        v-on:click="turnOff">
        Off
      </button>
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
      return this.$http.put(this.valueUrl, JSON.stringify(this.value == 'on')).then((response) => {
        this.error = '';
      }).catch((response) => {
        this.error = 'Failed to write value!';
      }).then(() => {
        this.loading = false;
      });
    },
    turnOn () {
      if (this.writable) {
        this.value = 'on';
        this.write();
      }
    },
    turnOff () {
      if (this.writable) {
        this.value = 'off';
        this.write();
      }
    }
  }
}
</script>
