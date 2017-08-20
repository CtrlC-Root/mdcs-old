<template>
  <div class="container">
    <h3 class="display-3 text-center">Dashboard</h3>

    <!-- Controls -->
    <div class="row">
      <!-- Control Cards -->
      <div class="col-sm-12 col-md-6 col-lg-4 my-2">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title">
              Office Brightness
              <button type="button" class="close" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </h4>
            <h6 class="card-subtitle mb-2 text-muted">hue-group-1:brightness</h6>
            <input type="range" min="1" max="254" step="1">
          </div>
        </div>
      </div>

      <div class="col-sm-12 col-md-6 col-lg-4 my-2">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title">
              Apartment Lights
              <button type="button" class="close" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </h4>
            <h6 class="card-subtitle mb-2 text-muted">hue-group-0:on</h6>
            <div class="btn-group" role="group" data-toggle="buttons" aria-label="Toggle State">
              <label class="btn btn-primary active">
                <input type="radio" autocomplete="off"> On
              </label>
              <label class="btn btn-primary">
                <input type="radio" autocomplete="off"> Off
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="col-sm-12 col-md-6 col-lg-4 my-2">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title">
              Group Name
              <button type="button" class="close" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </h4>
            <h6 class="card-subtitle mb-2 text-muted">hue-group-1:name</h6>
            <div class="input-group">
              <input class="form-control" type="text" value="Office">
              <span class="input-group-btn">
                <button class="btn btn-primary" type="button">Set</button>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Add New Card -->
      <div class="col-sm-12 col-md-6 col-lg-4 my-2">
        <div class="card card-template">
          <span>+</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'dashboard',

  data () {
    return {}
  },

  methods: {}
}
</script>

<style>
</style>
