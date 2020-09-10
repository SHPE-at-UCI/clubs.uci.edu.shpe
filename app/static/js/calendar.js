document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    navLinks: true,
    eventColor: 'light blue',
    themeSystem: 'bootstrap',
    googleCalendarApiKey: 'AIzaSyDKdchv03VdUKTbX7m00MMwnbj6x4-JCac',
    initialView: 'dayGridMonth',
    eventSources: {
      googleCalendarId: 'tech.shpeuci@gmail.com',
      textColor: "green"
    },
    
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },

  eventClick: function(info) {
    info.jsEvent.preventDefault();
  }
  
  });



  calendar.render();
});
