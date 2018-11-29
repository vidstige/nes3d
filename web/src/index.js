const jsnes = require('jsnes');
const romData = require('../../nes3d.nes');

const SCREEN_WIDTH = 256;
const SCREEN_HEIGHT = 240;

function Screen(canvas) {  
  const ctx = canvas.getContext('2d');
  const imageData = ctx.getImageData(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

  const buf = new ArrayBuffer(imageData.data.length);
  // Get the canvas buffer in 8bit and 32bit
  const buf8 = new Uint8ClampedArray(buf);
  const buf32 = new Uint32Array(buf);

  this.setBuffer = function(buffer) {
    var i = 0;
    for (var y = 0; y < SCREEN_HEIGHT; ++y) {
      for (var x = 0; x < SCREEN_WIDTH; ++x) {
        i = y * 256 + x;
        // Convert pixel from NES BGR to canvas ABGR
        buf32[i] = 0xff000000 | buffer[i]; // Full alpha
      }
    }
    
    imageData.data.set(buf8);
    ctx.putImageData(imageData, 0, 0);
  };
}
function ArrayBufferToString(buffer) {
  return String.fromCharCode.apply(null, Array.prototype.slice.apply(new Uint8Array(buffer)));
}

function ready(fn) {
  if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading"){
    fn();
  } else {
    document.addEventListener('DOMContentLoaded', fn);
  }
}


function start(romData) {
  const screen = new Screen(document.getElementById('tv'));

  // Initialize and set up outputs
  var nes = new jsnes.NES({
    onFrame: screen.setBuffer,
    onAudioSample: null
  });

  nes.loadROM(romData);

  var previous = null;
  function step(timestamp) {
    var dt = timestamp - previous;
    var fps = 60;
    if (dt > 1000/fps) {
      previous = timestamp;
      nes.frame();
    }
    requestAnimationFrame(step);
  }

  requestAnimationFrame(step);
}

ready(function() {
  fetch(romData).then(function(response) {
    return response.arrayBuffer();
  }).then(function(buffer) {
    const romData = ArrayBufferToString(buffer);
    start(romData);
  });
});
 
// Hook up whatever input device you have to the controller.
// nes.buttonDown(1, jsnes.Controller.BUTTON_A);
// nes.frame();
// nes.buttonUp(1, jsnes.Controller.BUTTON_A);
// nes.frame();
// ...