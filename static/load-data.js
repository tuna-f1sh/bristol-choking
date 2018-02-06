function changeFavicon(src) {
  $('link[rel="shortcut icon"]').attr('href', src)
}

$(document).ready(function(){
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.emit('ready');

  socket.on('data_loaded', function(json) {
    console.log(json);
    if (!json.error) {
      if (json.choking) {
        $(".jumbotron-heading").text("Yes");
        $(".lead").text(json.over40.join(", "))
        if (json.over40.length > 1) {
          $(".lead").append(" are choking")
        } else {
          $(".lead").append(" is choking")
        }
        changeFavicon('static/favicon-choking.ico');
      } else {
        $(".jumbotron-heading").text("No");
        $(".lead").text("Bristol is doing OK but could do better")
        changeFavicon('static/favicon-ok.ico');
      }
    } else {
      $(".jumbotron-heading").text("Opps");
      $(".lead").text("Something went wrong! Is the Bristol Air Quality site up?")
    }
    $(".loader-container").hide();
    $(".scraping-heading").hide();
    $(".status-heading").show();

    var cards = ["#wells-rd", "#parson-st", "#bristol-depot", "#fishponds"];
    var names = ["Wells Rd", "Parson St", "Bristol Depot", "Fishponds"];

    if (!json.error) {
      for (i = 0; i < cards.length; i++) {
        $(cards[i]).find('span.no2-15m').text(json.air_data[names[i]].NO215m)
        $(cards[i]).find('span.no2-24h').text(json.air_data[names[i]].NO224h)
        var minutes = Math.round(((json.time - json.air_data[names[i]].time) / 60) % 60)
        $(cards[i]).find('span.scrape-time').text(minutes);
        // if in area
        if (json.over40.indexOf(names[i]) != -1) {
          $(cards[i]).find('div.card-body').addClass("bg-danger text-white")
        }
        // if over 200
        if (json.over200.indexOf(names[i]) != -1) {
          $(cards[i]).find('[data-toggle="tooltip"]').tooltip();
          $(cards[i]).find('span.fa-exclamation-circle').show();
          // not in area otherwise text-warning
          if (json.over40.indexOf(names[i]) == -1) {
            $(cards[i]).find('p.no2-24h').addClass("text-danger")
          } else {
            $(cards[i]).find('p.no2-24h').addClass("text-warning")
          }
        }
      }
    } else {
      for (i = 0; i < cards.length; i++) {
        $(cards[i]).find('span.no2-15m').addClass("text-muted");
        $(cards[i]).find('span.no2-24h').addClass("text-muted");
      }
    }

    // $("div.album").animate({ opacity: 1 }, 400);
    $("div.album").show(400, function() {
    google.maps.event.trigger(mfishponds, 'resize')
    google.maps.event.trigger(mwellsrd, 'resize')
    google.maps.event.trigger(mbrisdepot, 'resize')
    google.maps.event.trigger(mparsonst, 'resize')
    });
  });
});
