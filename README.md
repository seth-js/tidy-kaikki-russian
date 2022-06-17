# tidy-kaikki-russian
Tidies up the JSON file initially provided by Kaikki.

This takes the data provided by <a href="https://kaikki.org/index.html">kaikki.org</a>, and tidies it up a bit so it's easier to use with other projects.

It's specifically been created for Russian, but you can modify the code to handle other languages.

These scripts require <a href="https://www.python.org/downloads/">Python 3.9.6</a> or newer and <a href="https://nodejs.org/en/">Node.js 14.16.1</a> or newer.

<h2>Instructions</h2>
<ol>
  <li>Download <a href="https://kaikki.org/dictionary/raw-wiktextract-data.json">this massive JSON file</a> (~13GB) from Kaikki.
    <br>Or download the <a href="https://kaikki.org/dictionary/raw-wiktextract-data.json.gz">compressed version</a> (~1.5GB) and extract it.
    <br>Either way, you'll now have a file called <code>raw-wiktextract-data.json</code>
  </li>
  <li>
    Download the repository, clone it, whatever.
  </li>
  <li>
    Move <code>raw-wiktextract-data.json</code> to the <code>Step 1</code> directory.
  </li>
  <li>
    Run <code>extract-language.py</code>.
  </li>
  <li>
    Move <code>ru-wikiextract.json</code> to the <code>Step 2</code> directory.
  </li>
  <li>
    Run <code>extract-lemmas.py</code>.
  </li>
  <li>
    Move <code>ru-lemmas.json</code> to the <code>Step 3</code> directory.
  </li>
  <li>
    Run <code>tidy-up.js</code>.
  </li>
</ol>

Inside the <code>Step 3</code> directory, you should now have a file called <code>ru-en-wiktionary-dict.json</code>.

This file should contain everything in a neat layout.
