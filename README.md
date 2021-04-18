# Sequential Links Rustler

<img width="45%" align="right" src="https://github.com/therden/links-rustler/blob/main/combined.png">

*Prepares and presents them tasty links just the way you like*

Website pages sometimes contain links -- other web pages, or image, video,
sound, or text files -- for which the files and/or directories are named using
numeric sequences.

When the design or organization of those pages makes accessing those resources a
chore, you might want to generate your own HTML page with links to a selected
subset of those resources.

That's where __Sequential Links Rustler__ comes in.


Getting Started
---------------
1.  Clone this repository, or download and extract [this zip file](https://github.com/therden/sequential-links-rustler/archive/refs/heads/main.zip)
2.  Change to the directory containing these files
3.  Run `python slr.py` or `python3 slr.py`
4.  In the GUI, fill in the URL mask (see examples below, and [here](`https://therden.github.io/sequential-links-rustler/-->), <!--set any desired options,--> click the _Rustle Up Some Links_ button, then sit back and wait (not long!) for your new web page to load.

<figure>
<img width="90%" align="center" src="assets/SLR_screenshot.png">
</figure>

Basic Usage
-----------
__Sequential Links Rustler__ accepts a __"URL mask"__ and generates an HTML page with links to the set of resources that were specified, opening the resulting file in a new browser tab.

A __URL mask__ is just like a standard URL, except that a __range definition__ has been substituted in place of a numeric value.

A minimal __range definition__ consists of a *Start* integer and a *Stop* integer, separated by a hyphen and surrounded by curly brackets.  __Sequential Links Rustler__ generates a series of links, each matching the __URL mask__, with the __range definition__ replaced by the next sequential value it defines.

For example, the URL mask

`https://therden.github.io/sequential-links-rustler/images/sausage{0-20}.jpeg`

includes the range definition `{0-20}`, and from it __Sequential Links Rustler__ will produce and load an HTML page that looks like

<figure>
<img width="90%" align="center" src="assets/Links_screenshot.png">
</figure>

__Sequential Links Rustler__ also supports sequences with declining values.

Changing the __range definition__ in the above example to `{20-0}` will generate the same page, but with the order of the images reversed.

__Sequential Links Rustler__ can generate sequences in which successive values differ by more than 1.  

Between the *Stop* value and the closing curly bracket, just insert a semi-colon and an integer representing the desired difference between consecutive values.

| range definition | set of values produced |
| ---------------- | ---------------------- |
| {0-9;2}          | 0, 2, 4, 6, 8          |
| {0-9;3}          | 0, 3, 6, 9             |
| {9-0;2}          | 9, 7, 5, 3, 1          |
| {9-0;3}          | 9, 6, 3, 0             |


Other Features
---------------
- zero padding

    | range_definition | sequence                |
    | ---------------- | ----------------------- |
    | {01-20;5}        | 01, 06, 11, 15          |
    | {020-001; 4}     | 020, 016, 012, 008, 004 |

- multiple range definitions within a __URL mask__

  For example: given the (partial), 3-level URL_mask `set{1-2}/subset{11-12}/pic{0-2}.jpg`, __Sequential Links Rustler__
  will produce the following (partial) link sequence

  set1/subset11/pic0.jpg<br>
  set1/subset11/pic1.jpg<br>
  set1/subset11/pic2.jpg<br>
  set1/subset12/pic0.jpg<br>
  set1/subset12/pic1.jpg<br>
  set1/subset12/pic2.jpg<br>
  set2/subset11/pic0.jpg<br>
  set2/subset11/pic1.jpg<br>
  set2/subset11/pic2.jpg<br>
  set2/subset12/pic0.jpg<br>
  set2/subset12/pic1.jpg<br>
  set2/subset12/pic2.jpg<br>

For more example URL masks and additional information about __Sequential Links Rustler__, see [the GitHub pages associated with this project](https://therden.github.io/sequential-links-rustler/).

ToDo
----
Bugs, ideas for improvements and new features are tracked in [Issues](https://github.com/therden/sequential-links-rustler/issues) -- feel free to share your thoughts there.

Speaking of contributions
-------------------------
It isn't required (of course), but if you find this project useful and are so moved, you can

<a href="https://www.buymeacoffee.com/tomherden" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="217px" ></a>

__Buy Me a Coffee__ is a great way to publicly support creators.  It's quick, easy, and your contribution is recorded and made visible.  (You _can_ choose to make your donation private if you prefer.)

Credits
-------
<img width="125px" align="right" src="logo.png">

Thanks to [MikeTheWatchGuy](https://github.com/MikeTheWatchGuy) for creating and maintaining [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI).

And also to Quinn for his encouragement.

The original source of the three black sausages that I incorporated into the logo of "The Rustler" was the SVG found at [Sausage by Jacob Halton from the Noun Project](https://thenounproject.com/term/sausage/4135/)


<!--
WAV files for 'Countdown' example from Evolution/Voxeo's [open source (LPGL) 'Numbers' audio prompts library in open source (LPGL) tools library](https://evolution.voxeo.com/library/audio/prompts/)
-->
