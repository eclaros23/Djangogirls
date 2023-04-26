document.getElementById("titlelink")

let element = document.getElementById("titlelink");

element.style["color"] = "aqua";
element.style["border"] = "3px solid aqua";

function doTheStuff() { //defining a python function
  let elements_posttitles = document.getElementsByClassName("posttitle");

for (element of elements_posttitles){
  element.style["border"] = "3px solid green";
  
  }
}

let theButton = document.getElementById("thebutton");
theButton.addEventListener("click", doTheStuff);

var flyingMen = [];

var button = document.getElementById('emojibutton');
var textvalue = "Caktus Group 😊🌵";
var fontsize = "24";
//emoji object
  function emoji(face, startx, starty, flour, fs, flyUpMax) {
    this.isAlive = true;
    this.face = face;
    this.x = startx;
    this.y = starty;
    this.flourLevel = flour;
    this.increment = -Math.floor((Math.random()*flyUpMax)+10);
    this.xincrement = Math.floor((Math.random()*10)+1);
    this.xincrement *= Math.floor(Math.random()*2) == 1 ? 1 : -1;
    this.element = document.createElement('div');
    this.element.innerHTML = face;
    this.element.style.position = "absolute";
    this.element.style.fontSize = fs + "px";
    this.element.style.color = "black";
    document.getElementById("fa").appendChild(this.element);

    this.refresh = function(){
      console.log(this.isAlive)
      if (this.isAlive) {
        //------Y axis-----
        
        
        
        
        this.y += this.increment;
        this.x += this.xincrement;
        this.increment += 0.25;
        
        if (this.y >= this.flourLevel) {
          if (this.increment <=5) {
            this.isAlive = false;
          }
         this.increment = -this.increment + 5;
        }
        
        this.element.style.transform = "translate(" + this.x + "px, " + this.y + "px)";
      } else {
        this.element.style.transform = "translate(px, px)";
      }
    }
    
  }



button.addEventListener("click", goB);


function goB() {
  console.log(fontsize);
  console.log("fontsize");
  console.log(button.getBoundingClientRect());
  console.log("button.getBoundingClientRect");
  var xv = (button.getBoundingClientRect().left + button.clientWidth/2) - (fontsize/2);
  var yv = (button.getBoundingClientRect().top + button.clientHeight/2) - (fontsize/2);
  var fl = button.getBoundingClientRect().top + 100;
  var face = textvalue;
  console.log("xv: ", xv);
  console.log("yv: ", yv);
  console.log("fl: ", fl);
  console.log("face: ", face);
  for (var i = 0; i < 50; i++) {
    var coolGuy = new emoji(face, xv, yv, fl, fontsize, 12);
    flyingMen.push(coolGuy);
  }

}



//Rendering
function render() {
  for (var i = 0; i < flyingMen.length; i++) {
    if (flyingMen[i].isAlive == true) {
      flyingMen[i].refresh();
    } else {
      flyingMen[i].element.remove();
      flyingMen.splice(i, 1);
    }
  }
  requestAnimationFrame(render);
}

render();

