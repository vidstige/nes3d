const jsnes = require('jsnes');
const romData = require('../../nes3d.nes');

// Initialize and set up outputs
var nes = new jsnes.NES({
  onFrame: function(frameBuffer) {
    console.log(typeof frameBuffer);
  },
  onAudioSample: null
});

function ArrayBufferToString(buffer) {
  return String.fromCharCode.apply(null, Array.prototype.slice.apply(new Uint8Array(buffer)));
}

var previous = null;
function step(timestamp) {
  var dt = timestamp - previous;
  var fps = 1;
  if (dt > 1000/fps) {
    previous = timestamp;
    console.log(dt);
    //console.log(nes);
    nes.frame();
  }
  requestAnimationFrame(step);
}


fetch(romData).then(function(response) {
  return response.arrayBuffer();
}).then(function(buffer) {
  const romData = ArrayBufferToString(buffer);
  nes.loadROM(romData);
  requestAnimationFrame(step);
});
 
// Hook up whatever input device you have to the controller.
// nes.buttonDown(1, jsnes.Controller.BUTTON_A);
// nes.frame();
// nes.buttonUp(1, jsnes.Controller.BUTTON_A);
// nes.frame();
// ...