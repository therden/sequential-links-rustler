# GitHub Page(s) for __Sequential Links Rustler__

This file is saved in the repo's `\docs` subdirectory, which is the source for the project's `Github Pages`.

Subirectories and other files saved under `\docs` are used in both README.md and in this file to illustrate how `Sequential Links Rustler` works.


More example __URL masks__
----
Sequential links with values declining by 1<br>
<input type="text" size="52ch" value="https://therden.github.io/sequential-links-rustler/png_numbers/{5-0}.png" id="Ex1">
<button onclick="copyEx1()">Copy</button>
<script>
function copyEx1() {
  var copyText = document.getElementById("Ex1");
  copyText.select();
  document.execCommand("copy");
}
</script>

Sequential links with values declining by 2<br>
<input type="text" size="52ch" value="https://therden.github.io/sequential-links-rustler/png_numbers/{5-0;2}.png" id="Ex2">
<button onclick="copyEx2()">Copy</button>
<script>
function copyEx2() {
  var copyText = document.getElementById("Ex2");
  copyText.select();
  document.execCommand("copy");
}
</script>

Three-level embedded __range definition__s<br>
<input type="text" size="70ch" value="https://therden.github.io/sequential-links-rustler/gallery/{01-02}/set{1-2}/thumbnail_{0-1}.jpeg" id="Ex3">
<button onclick="copyEx3()">Copy</button>
<script>
function copyEx3() {
  var copyText = document.getElementById("Ex3");
  copyText.select();
  document.execCommand("copy");
}
</script>


Thousands of links, only some of which actually exist<br>
<input type="text" size="95ch" value="http://vision.stanford.edu/aditya86/ImageNetDogs/thumbnails/n02098286-West_Highland_white_terrier/n02098286_{0-6516;1}.jpg" id="Ex4">
<button onclick="copyEx4()">Copy</button>
<script>
function copyEx4() {
  var copyText = document.getElementById("Ex4");
  copyText.select();
  document.execCommand("copy");
}
</script>


<!--- `https://therden.github.io/sequential-links-rustler/png_numbers/{100-120;4}.html`--->
<!--- `https://evolution.voxeo.com/library/audio/prompts/numbers/{0-10;1}.wav`-->
