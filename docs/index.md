This file is saved in the `\docs` subdirectory of [the Sequential Links Rustler repository on GitHub](https://github.com/therden/sequential-links-rustler).

Other files have been saved within subdirectories of `\docs` to demonstrate __Sequential Links Rustler__ in action.

Advanced sequence definitions
-----------------------------

- ### zero padding of sequence values

    When a website's numeric values include leading zeros, just include those zeros in your sequence definition.

    | sequence_definition | produces sequence       |
    | ------------------- | ----------------------- |
    | {01-05}             | 01, 02, 03, 04, 05      |
    | {000-004}           | 000, 001, 002, 003, 004 |


- ### declining values within a sequence

    Within the sequence definition, make *Start* the larger and *Stop* the smaller value.

    | sequence_definition | produces sequence |
    | ------------------- | ------------------|
    | {5-0}               | 5, 4, 3, 2, 1, 0  |
    | {15-13}             | 15, 14, 13        |    

- ### custom intervals between values

    Between the *Stop* value and the closing curly bracket, insert a semi-colon and an integer representing the distance between consecutive values.

    | sequence definition | set of values produced |
    | ------------------- | ---------------------- |
    | {0-9;2}             | 0, 2, 4, 6, 8          |
    | {0-9;3}             | 0, 3, 6, 9             |

    Custom intervals can be combined with declining values:

    | sequence definition | set of values produced |
    | ------------------- | ---------------------- |
    | {9-0;2}             | 9, 7, 5, 3, 1          |
    | {9-0;3}             | 9, 6, 3, 0             |

- ### including multiple sequence definitions within a single URL mask

    Given the (partial) URL_mask, `foo{001-002}/bar{12-9;3}/pic{0-10;5}.jpg`
    __Sequential Links Rustler__ would produce the following sequence of (partial) links. (Blank lines added to make it easier to see the sequence patterns.)

    foo001/bar12/pic0.jpeg<br>
    foo001/bar12/pic5.jpeg<br>
    foo001/bar12/pic10.jpeg<br>

    foo001/bar9/pic0.jpeg<br>
    foo001/bar9/pic5.jpeg<br>
    foo001/bar9/pic10.jpeg<br>

    foo002/bar12/pic0.jpeg<br>
    foo002/bar12/pic5.jpeg<br>
    foo002/bar12/pic10.jpeg<br>

    foo002/bar9/pic0.jpeg<br>
    foo002/bar9/pic5.jpeg<br>
    foo002/bar9/pic10.jpeg<br>

    __Note:  The above example combines zero-padded `foo` values, `bar` values which decline by 3, and `pic` values which ascend by 5.__

More example URL masks
----------------------
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

Three-levels of embedded range definitions<br>
<input type="text" size="70ch" value="https://therden.github.io/sequential-links-rustler/levels/gallery{01-02}/set{1-2}/thumbnail_{0-1}.jpeg" id="Ex3">
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
