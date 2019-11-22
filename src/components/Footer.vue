<template>
  <footer>
    <b-navbar class="footer" fixed="bottom" type="light" sticky>
      <b-navbar-nav>
        <b-nav-item class="content">Copyright &copy; 2019 Pilgrimage Software</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown text="Lang" right dropup>
          <b-dropdown-item href="#">EN</b-dropdown-item>
          <b-dropdown-item href="#">ES</b-dropdown-item>
          <b-dropdown-item href="#">RU</b-dropdown-item>
          <b-dropdown-item href="#">FA</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item class="content">Help</b-nav-item>
        <b-nav-item class="content">v1.0</b-nav-item>
      </b-navbar-nav>
    </b-navbar>
  </footer>
</template>

<script>
</script>

<style>
footer {
  background-color: #f8f8f8;
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 60px;
  /* vertical-align: middle; */
  /* margin-left: 10px; */
}
</style>
