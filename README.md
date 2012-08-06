### What is Sikwidgets?
Ever wanted to programmatically control an application, but you didn't have access to the source?

Sikwidgets is a Python framework built on top of [Project Sikuli](http://sikuli.org). Sikuli allows users to specify images of the screen that can be clicked, hovered over, or typed into. Sikwidgets builds on this concept by allowing users to define how an application actually looks in terms of widgets as opposed to just images. For example, rather than saying:

```
type(image-of-text-field, "hello world")
```

We can now say:

```
text_field.text = "hello world"
```

By considering a widget to be a section of the screen that can have multiple states (ie, enabled, disabled, focused, etc.), Sikwidgets reduces the amount of code necessary to write to handle more advanced GUIs.

The primary goal of Sikwidgets is to provide a robust framework for automating the usage of advanced applications that have many widgets and require a more structured approach to controlling them.

### Installing
First, install the most recent version of Sikuli (1.0rc3 at the time of writing).
Then,

On Windows (in Git Shell using PowerShell, preferably):

```
$ git clone git://github.com/griffy/sikwidgets.git
$ cd sikwidgets\install
$ .\install.bat
```

Now you're good to go!

### Example Usage
Let's go through the steps of creating our very own Sikwidgets application.

Sikwidgets comes with its own script, sikwidgets, to make our lives easier. Rather than needing to create a new project structure every time, we can tell the sikwidgets script to do that for us.

```
$ sikwidgets.bat --new demo
```

Now you'll notice that the script has generated a demo folder with the following contents:

```
images/
windows/
windows/demo_window.py
demo.py
```

**To Be Continued**

Perhaps the nicest feature of the sikwidgets script is that it enables us to use Sikuli's screen capture utility for our widgets. If we do the following in our project directory:

```
$ sikwidgets.bat --capture demo
```

The script will look for an application called Demo in a demo.py file and call capture_screenshots on each window in the application. Each window will, in turn, call capture_screenshots on each widget it contains. The result is that you can define your application in code, then simply execute this script to capture the corresponding screenshots necessary for your widgets.

If you don't need to take screenshots of every widget, you can use a scoping pattern similar to URIs:

```
app/window/[window ...]/[page ...]/widget
```

So, if we do:

```
$ sikwidgets.bat --capture demo/demo_window/demo_button
```

Only demo_button inside DemoWindow will have its capture_screenshots method called.

Finally, if we don't have a widget defined in code yet, but we want to capture a screenshot nonetheless and dump it to a file, we can do that too!

```
$ sikwidgets.bat --screenshot [\path\to\]name
```

Once the screenshot is taken, it will be saved to [\path\to\\]name.png

If you want to look at some real examples of what can be done, check out the sikwidgets/examples folder. To run one, just do:

```
$ cd sikwidgets\examples
$ .\run.bat example-folder-name
```

### License
Sikwidgets is released under the MIT License, so feel free to use it in your projects!