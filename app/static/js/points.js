var winterPoints = document.getElementById('winter');
var winterMinus = document.getElementById('winterM');
var winterPlus = document.getElementById('winterP');

var fallPoints = document.getElementById('fall');
var fallMinus = document.getElementById('fallM');
var fallPlus = document.getElementById('fallP');

var springPoints = document.getElementById('spring');
var springMinus = document.getElementById('springM');
var springPlus = document.getElementById('springP');

winterMinus.addEventListener("click", () => {subPoints(winterPoints);} );
winterPlus.addEventListener("click", () => {addPoints(winterPoints);} );

fallMinus.addEventListener("click", () => {subPoints(fallPoints);} );
fallPlus.addEventListener("click",  () => {addPoints(fallPoints);} );

springMinus.addEventListener("click", () => {subPoints(springPoints);} );
springPlus.addEventListener("click", () => {addPoints(springPoints);} );

function subPoints(e){
  points = e.value;
  if(points > 0){
    points--;
  }
  e.value = points;
}


function addPoints(e){
  e.value++;
}
