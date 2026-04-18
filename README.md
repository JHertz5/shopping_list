# shopping_list
Python script to automate shopping list creation

This is a python script to automate the process of creating a shopping list. The script pulls shopping list data from a Google Sheets spreadsheet. This data consists of Ingredients, Recipes, and Input. These are pretty self explanatory if you look at the spreadsheet. Once the data has been collected and processed, the shopping list used to create a [todo.txt](https://github.com/todotxt/todo.txt) file in a location local to your device.

## Android Set Up
The expected use case for this project is to run on an Android device. Follow the following steps prior to following the steps listed in [Generic Set Up](#generic-set-up).
1. Install [Termux](https://f-droid.org/en/packages/com.termux/) (a Linux terminal emulator). In Termux, run the following commands:
2. In Termux, run `pkg install git make python` to install supporting Linux programs.
3. In Termux, run `termux-setup-storage` to set-up access from Termux to main Android storage. This enables you to set the shopping list generator to write to a file that is visible to your todo.txt app.
4. In Termux, run `pkg install python-cryptography`. This is a dependency of gspread that needed rust and took ages to install when via `pip`, so installed it ahead of time saves some hassle.

## Generic Set Up
These rules can be run from a Linux device.
1. Clone the repository.
2. Install python dependencies - in the root of the repository, run `make init`.
3. Create a [Google Sheets spreadsheet in this format](https://docs.google.com/spreadsheets/d/1B3kR0sYUVmMu2IA-XWe45FsB8voRAKXCzPxGnjfMUiI/edit?usp=sharing).
3. Set up access to your spreadsheet. Here are some [instructions to get credentials for spreadsheet API access](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account). This produces a token file which must be stored on the same device from which shopping_list will be run.
    - The `make list` command (see [Usage](#usage) for more details) assumes that your shopping list file is called "Shopping List" and that your token file is stored in the root directory of the clone.
    - If this is not the case, you can run the shopping list script (`./bin/shopping_list`) directly. In this case, the path to the token must be provided as the `-t` argument, while the name of the spreadsheet must be provided as the `-s` argument.
4. Install any [todo.txt](http://todotxt.org/) compatible app, e.g. [SimpleTask](https://github.com/mpcjanssen/simpletask-android/) if on Android (although SimpleTask is heartbreakingly no longer maintained or available on f-droid. It must be downloaded through the [APK](https://fxedel.gitlab.io/fdroid-website/en/packages/nl.mpcjanssen.simpletask/)). Once you have a script-generated output file (provided to the shopping list script with the `-g` argument), you'll need to set this app up to use that file.

> [!NOTE]
> On Android 13 and above, file access permissions may prevent SimpleTask from accessing non-media files. To work around this, save your todo list file with a media file extension (e.g. `.mp3`) so SimpleTask can access it.

## Usage
1. Run `make list` in the root of the repo.
2. Follow the prompts in the script.
3. Open the file (provided with the `-g` argument) within the todo.txt app.

## Spreadsheet Format
TODO
