$.sidebarMenu = function(menu) {
  var animationSpeed = 300;
  
  $(menu).on("click", "li a", function(e) {
    var $this = $(this);
    var checkElement = $this.next();

    if (checkElement.is(".treeview-menu") && checkElement.is(":visible")) {
      checkElement.slideUp(animationSpeed, function() {
        checkElement.removeClass("menu-open");
      });
      checkElement.parent("li").removeClass("active");
    } else if (checkElement.is(".treeview-menu") && !checkElement.is(":visible")) {
      var parent = $this.parents("ul").first();
      var ul = parent.find("ul:visible").slideUp(animationSpeed);
      ul.removeClass("menu-open");
      var parent_li = $this.parent("li");

      checkElement.slideDown(animationSpeed, function() {
        checkElement.addClass("menu-open");
        parent.find("li.active").removeClass("active");
        parent_li.addClass("active");
      });
    }

    if (checkElement.is(".treeview-menu")) {
      e.preventDefault();
    }
  });
};

$.sidebarMenu($(".sidebar-menu"));

jQuery(function ($) {
  // Toggle sidebar
  $(".toggle-sidebar").on("click", function () {
    $(".page-wrapper").toggleClass("toggled");
  });

  // Pin sidebar on click
  $(".pin-sidebar").on("click", function () {
    if ($(".page-wrapper").hasClass("pinned")) {
      $(".page-wrapper").removeClass("pinned");
      $("#sidebar").unbind("hover");
    } else {
      $(".page-wrapper").addClass("pinned");
      $("#sidebar").hover(
        function () {
          $(".page-wrapper").addClass("sidebar-hovered");
        },
        function () {
          $(".page-wrapper").removeClass("sidebar-hovered");
        }
      );
    }
  });

  // Toggle sidebar overlay
  $("#overlay").on("click", function () {
    $(".page-wrapper").toggleClass("toggled");
  });

  // Window resizing actions
  $(window).resize(function () {
    if ($(window).width() <= 768) {
      $(".page-wrapper").removeClass("pinned");
    }
  });
  $(window).resize(function () {
    if ($(window).width() >= 768) {
      $(".page-wrapper").removeClass("toggled");
    }
  });
});

$(function () {
  $("#loading-wrapper").fadeOut(2000);
});

$(function () {
  $(".day-sorting .btn").on("click", function () {
    $(".day-sorting .btn").removeClass("btn-primary");
    $(this).addClass("btn-primary");
  });
});

var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Popover
var popoverTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="popover"]')
);
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});


