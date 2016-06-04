# WolframAplha CLI

Command Line Interface to run queries on [WolframAlpha](http://www.wolframalpha.com/)

# Installation
Clone the repository and run inside its folder:

    pip install --user .

Be aware you need ~/.local/bin/ in your $PATH to run locally installed pip packages.

# Configuration
In order to run WolframAlpha CLI you'll need an API key:

1. Go to [WolframAlpha's Developer Portal](https://developer.wolframalpha.com/portal/signup.html) and sign up

2. Log in, proceed to [My Apps](http://developer.wolframalpha.com/portal/myapps/) and click "Get an AppID"

3. Run ````wa-cli --set-key KEY```` with your key

In case you want to check other options, run ````wa-cli --config```` to edit the config file.

# Usage
To enter the REPL just run ````wa-cli````.

Once inside the REPL, some responses may provide pictures. To open all pictures at once, type ````:allpics````.

You can also run ````:open```` to open the last query in your browser.

In case you prefer single queries, use the -q option:

    wa-cli -q "Your query"


# License
The MIT License (MIT)

Copyright (c) 2014 Fernando

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
