<template>
  <div class="page-container">
    <md-toolbar class="md-warn main">
      <h1 class="md-title">Guick Guide</h1>
    </md-toolbar>
    <div class="content">
      <h3>1. Open <a href="/app" target="_blank">BassApp Editor</a></h3>
      <h3>2. Create project</h3>
      <p>
        Typically, you should be working on your project locally, saving it in your browser's storage.
        It is highly recommended to regulary save your changes. 
      </p>
      <p>
        More information about editing can be found in built-in user manual (icon at bottom-right corner),
        or in <a href="https://www.youtube.com/watch?v=JLsOd2502jM">video tutorial</a> from MannyBass (it's older video, but not so many things has changed).
      </p>

      <h3>3. Upload project</h3>
      <p>Once is your project ready for publishing and you have registred account, you can upload it here on BassCloud.
      </p>
      <h3>4. Project updating</h3>
      <p>
        Authors can update their projects either by:
        <ul>
          <li>repeating upload process (from BassApp, after changes in composition)</li>
          <li>editing information about project directly from BassCloud project page</li>
        </ul>
      </p>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'guide'
  }
</script>

<style lang="scss" scoped>
  .align-right {
    margin-left: auto;
    margin-right: 0;
  }
  .content {
    padding: 16px;
    max-width: 600px;
  }
</style>
