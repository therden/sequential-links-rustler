# Sequential Links Rustler

<img width="45%" align="right" src="https://github.com/therden/links-rustler/blob/main/combined.png">

*Prepares and presents them tasty links just the way you like*

Website pages sometimes contain links -- other web pages, or image, video,
sound, or text files -- for which the files and/or directories are named using
numeric sequences.

When the design or organization of those pages makes accessing those resources a
chore, you might want to generate your own HTML page with links to a selected
subset of those resources.

That's where `Sequential Links Rustler` comes in.


Getting Started
---------------
1.  Clone this repository, or download and extract [this zip file](https://github.com/therden/sequential-links-rustler/archive/refs/heads/main.zip)
2.  Change to the directory containing these files
3.  Run `python slr.py` or `python3 slr.py`
4.  In the GUI, fill in the URL mask (see examples below<!--, and more [here](`https://therden.github.io/sequential-links-rustler/-->) and click the button labeled _Rustle Up Some Links_, <!--set any desired options,--> then sit back and wait (not long!) for your new web page to load.

<figure>
<img width="90%" align="center" src="assets/SLR_screenshot.png">
</figure>

Basic Usage
-----------
`Sequential Links Rustler` takes a __"URL mask"__ -- which is really just a URL with one or more "range definitions" -- and generates an HTML page with links to the set of resources that were specified, opening it in a new tab withing the browser you've selected.

__"Range definitions"__ are contained within curly brackets, and consist (at a minimum) of a Start integer and a Stop integer separate by a hyphen.  (If desired, those elements may be followed by a semi-colon and a Stride value, which may be a positive or negative integer value.  If no Stride is specified, a positive value of 1 will be assumed.)

For example: the URL mask<br>
`https://therden.github.io/sequential-links-rustler/images/sausage{0-20}.jpeg`<br>
contains the range definition `{0-20}` and produces and loads an HTML page that looks like

<figure>
<img width="90%" align="center" src="assets/Links_screenshot.png">
</figure>


Features
--------
The range definition shown above generated a sequence of links that were incremented by one; but `Sequential Links Rustler` is flexible.  In addition to that default behavior, it supports
- sequences with gaps > 1 between values (aka 'skipping' integers.)
    - the range definition `{0-7;2}` will produce links with the values `0, 2, 4, 6`
    - the range definition `{0-7;3}` will produce links with the values `0, 3, 6`    
- sequences with values declining by one or more integers
    - the range definition `{7-0;-2}` will produce links with the values `7, 5, 3, 1`
    - the range definition `{7-0;-3}` will produce links with the values `7, 4, 1`    
- zero padding
    - the range definition `{01-10;1}` will produce links with the values `01, 02, 03, 04, 05, 06, 07, 08, 09, 10`
    the range definition `{001-010}` will produce links with the values `001, 002, 003, 004, 005, 006, 007, 008, 009, 010`
- multiple range definitions within a single URL mask
    - copy the following into `Sequential Links Rustler` and hover over the images in order to see how the three range definitions are processed recursively, left-to-right.
    `https://therden.github.io/sequential-links-rustler/levels/gallery{01-03;1}/set{1-2;1}/thumbnail_{3-0;-1}.jpeg`

Other example URL-masks
-----------------------
- `https://therden.github.io/sequential-links-rustler/png_numbers/{5-0;-1}.png`
- `https://therden.github.io/sequential-links-rustler/png_numbers/{100-120;4}.html`
- `http://vision.stanford.edu/aditya86/ImageNetDogs/thumbnails/n02098286-West_Highland_white_terrier/n02098286_{0-6516;1}.jpg`
<!--- `https://evolution.voxeo.com/library/audio/prompts/numbers/{0-10;1}.wav`-->

ToDo
----
I'm tracking ideas for features and improvements (along with bugs) in this repo's [Issues](https://github.com/therden/sequential-links-rustler/issues) -- feel free to make your own contributions.

Speaking of contributions
-------------------------
It isn't required (of course), but if you find this project useful and are so moved, you can

<a href="https://www.buymeacoffee.com/tomherden" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="217px" ></a>

__Buy Me a Coffee__ is a great way to publicly support creators.  It's quick, easy, and your contribution is recorded so that others can see that you've made a contribution.  (You can choose to make your donation private if you prefer.)

Credits
-------
<img width="125px" align="right" src="logo.png">

Thanks to [MikeTheWatchGuy](https://github.com/MikeTheWatchGuy) for creating and maintaining [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI).

And also to Quinn for his encouragement (constructive criticism to come?)

The source of the three black sausages incorporated into the image of "the Rustler" was the SVG at [Sausage by Jacob Halton from the Noun Project](https://thenounproject.com/term/sausage/4135/)


<!--
WAV files for 'Countdown' example from Evolution/Voxeo's [open source (LPGL) 'Numbers' audio prompts library in open source (LPGL) tools library](https://evolution.voxeo.com/library/audio/prompts/)
-->
