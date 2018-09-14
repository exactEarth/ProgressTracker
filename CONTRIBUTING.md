# Contributing to progress_tracker

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to `progress_tracker`, which are hosted in the [exactEarth Organization](https://github.com/exactEarth) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

- [Contributing to progress_tracker](#contributing-to-progress_tracker)
            - [Table Of Contents](#table-of-contents)
    - [I don't want to read this whole thing I just have a question!!!](#i-dont-want-to-read-this-whole-thing-i-just-have-a-question)
    - [Design Philosophy](#design-philosophy)
    - [How Can I Contribute?](#how-can-i-contribute)
        - [Reporting Bugs](#reporting-bugs)
            - [Before Submitting A Bug Report](#before-submitting-a-bug-report)
            - [How Do I Submit A (Good) Bug Report?](#how-do-i-submit-a-good-bug-report)
        - [Suggesting Enhancements](#suggesting-enhancements)
            - [Before Submitting An Enhancement Suggestion](#before-submitting-an-enhancement-suggestion)
            - [How Do I Submit A (Good) Enhancement Suggestion?](#how-do-i-submit-a-good-enhancement-suggestion)
        - [Developing progress_tracker code](#developing-progress_tracker-code)
            - [General Workflow](#general-workflow)
            - [Terminology](#terminology)
                - [Casual description](#casual-description)
            - [Coding Style](#coding-style)
                - [Visual Studio Code](#visual-studio-code)
            - [Supported Python Versions](#supported-python-versions)
            - [Supported Operating Systems](#supported-operating-systems)
            - [Functional Testing](#functional-testing)
            - [Documentation](#documentation)
            - [Pull Requests](#pull-requests)

## I don't want to read this whole thing I just have a question!!!

Sure. First [search the existing issues](https://github.com/exactEarth/ProgressTracker/issues?utf8=%E2%9C%93&q=is%3Aissue) to see if one of the existing issues answers it. If not, simply [create an issue](https://github.com/exactEarth/ProgressTracker/issues/new) and ask your question.

## Design Philosophy

progress_tracker's goal is to be the fastest ISO 8601 parser available for Python. It probably will never support the complete grammar of ISO 8601, but it will be correct for the chosen subset of the grammar. It will also be robust against non-conforming inputs. Beyond that, performance is king. 

That said, some care should still be taken to ensure cross-platform compatibility and maintainability. For example, this means that we do not hand-code assembly instructions for a specific CPUs/architectures, and instead rely on the native C compilers to take advantage of specific hardware. We are not against the idea of platform-specific code in principle, but it would have to be shown to be produce sufficient benefits to warrant the additional maintenance overhead.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for progress_tracker. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:.

Before creating bug reports, please check [this list](#before-submitting-a-bug-report) as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report).

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Before Submitting A Bug Report

* **Perform a [cursory search](https://github.com/exactEarth/ProgressTracker/issues?utf8=%E2%9C%93&q=is%3Aissue)** to see if the problem has already been reported. If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). Create an issue on the repository and provide the following information.

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include snippets of code that reproduce the problem (Make sure to use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines) so that it gets formatted in a readable way).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.

Include details about your configuration and environment:

* **Which version of progress_tracker are you using?** You can get the exact version by running `pip list` in your terminal. If you are not using [the latest version](https://github.com/exactEarth/ProgressTracker/releases), does the problem still happen in the latest version?
* **What's the name and version of the OS you're using**?

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for progress_tracker, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag_right:.

Before creating enhancement suggestions, please check [this list](#before-submitting-an-enhancement-suggestion) as you might find out that you don't need to create one. When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion).

#### Before Submitting An Enhancement Suggestion

* **Perform a [cursory search](https://github.com/exactEarth/ProgressTracker/issues?utf8=%E2%9C%93&q=is%3Aissue)** to see if the enhancement has already been suggested. 

If it has, don't create a new issue. Consider adding a :+1: [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the issue description. If you feel that your use case is sufficiently different, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/). Create an issue on the repository and provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Explain why this enhancement would be useful** to most progress_tracker users and therefore should be implemented in progress_tracker.
* **List some other libraries where this enhancement exists** (if you know of any).
* **Specify which version of progress_tracker you're using.** You can get the exact version by running `pip list` in your terminal. If you are not using [the latest version](https://github.com/exactEarth/ProgressTracker/releases), is the enhancement still needed in the latest version?
* **Specify the name and version of the OS you're using.**

### Developing progress_tracker code

#### General Workflow

progress_tracker uses the same contributor workflow as many other projects hosted on GitHub.

1. Fork the [progress_tracker repo](https://github.com/exactEarth/ProgressTracker) (so it becomes `<yourname>/ProgressTracker`).
2. Clone that repo (`git clone https://github.com/<yourname>/ProgressTracker.git`).
3. Create a new branch (`git checkout -b my-descriptive-branch-name`).
4. Make your changes and commit to that branch (`git commit`).
5. Push your changes to GitHub (`git push`).
6. Create a Pull Request within GitHub's UI.

See [this guide](https://opensource.guide/how-to-contribute/#opening-a-pull-request) for more information about each step.

#### Terminology

When writing both code and documentation for progress_tracker, it is important to apply consistent terminology.

This terminology is to be applied consistently to both the code and the docs, with some minor exceptions possible for introductory/casual portions of the docs (or similar).

Perhaps the easiest way to demonstrate the terminology, is to simply use the terms in a casual description (if there is still confusion/ambiguity, feel free to create an issue to discuss/ask about it).

##### Casual description

`track_progress` reports the progress of processing an **iterable** (or **stream**) of **records**.

Progress **conditions** are **met** which **trigger** the **creation** of **reports**. By default a **report** causes a message to be printed to `stdout`.


#### Coding Style

progress_tracker's coding style largely adheres to the [Python PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.

progress_tracker makes use of [autopep8](https://pypi.org/project/autopep8/) to make this mostly automatic. The auto-formatting rules are defined in the [setup.cfg](setup.cfg) file. 

progress_tracker also makes use of [Python's Type Annotations](https://www.python.org/dev/peps/pep-0484/). It uses [Mypy](http://mypy-lang.org/) to automatically perform static analysis on these types.

##### Visual Studio Code

If you are using Visual Studio Code as your editor, you can use the ["Python"](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension. 

* Set the `"editor.formatOnSave": true` setting to automatically auto-format the code on saves.
* Set the `"python.linting.mypyEnabled": true` setting to automatically run `mypy` on the code on saves.

#### Supported Python Versions

progress_tracker is built with, and tested against, cPython versions 3.6+ (for the full list see the [README](README.rst)). Please make sure that you do not accidentally make use of features that are specific to certain versions of Python. Feel free to make use of modern features of the languages, but you also need to provide mechanisms to support the other versions as well.

#### Supported Operating Systems

progress_tracker supports running on multiple operating systems, including Windows. Make sure to test changes on both a Windows (MSVC) and Linux (gcc) machine to ensure compatibility.

#### Functional Testing

progress_tracker's functionality/unit tests are found in the [tests/test_progress_tracker.py](tests/test_progress_tracker.py) file. The `python setup.py test` command can be used to run the tests.

Any new functionality being developed for progress_tracker should also have tests being written for it. Tests should cover both the "sunny day" (expected, valid input) and "rainy day" (invalid input or error) cases.

#### Documentation

All changes in functionality should be documented in the [`README.rst`](README.rst) file. Note that this file uses the [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) format, since the file is rendered as part of [progress_tracker's entry in PyPI](https://pypi.org/project/progress_tracker/), which only supports reStructuredText.

You can check your reStructured text for syntax errors using (restructuredtext-lint)[https://github.com/twolfson/restructuredtext-lint]:

```
pip install Pygments restructuredtext-lint
rst-lint --encoding=utf-8 README.rst
```

#### Pull Requests

* Follow the [Code](#coding-style) style guide.
* Document new code and functionality [See "Documentation"](#documentation)

