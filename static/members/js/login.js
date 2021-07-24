function fadeOut() {
  $(".alert").fadeToggle(500, "swing", function () {
    this.remove();
  });
}

var delay = 3000; //3 seconds
setTimeout(fadeOut, delay);
