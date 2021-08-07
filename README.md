# `strans` Strings transformations for NIXers

You probably used those NIX programs that let you transform text in the daily work. 
Probably you have your own set of favourite tools ... the `sed`  to replace strings, the `awk` do some more formatting, `cut` - to pick a field ... ah how useful is that one!
But each of them is a bit different, has own syntax of commands, specialities .... well, the history.
What if there would be one simple program that would let you do all the transformation we usually need to do - and if not you can extend it.

An example:
Say, that you want to list PDF files in the directory and generate LATEX includegraphics directive for them. Here it is:
```
ls  | strans "split | cont pdf |cont _q| prep \includegraphics{ | app } | nl"
```
So it starts with the `ls` that outputs all the file names to stdout. Then `strans` picks up and:
* `split` - splits what the `ls` gives into a list
* `cont pdf` - selects those files that have `pdf` in the name (you could have used `grep`)
* `cont _q` - selects those containing `_q` (because why not, I want those - and it nicely shows that you can combine the strans commands) (again can `grep` for it)
* `prep \include..` - prepends the text to each file name (`awk` probably)
* `app }` - well, appends the text (ok, can be also `awk`-ed)
* `nl` - outputs the list of elements, each in new line (`ls -1` would do)

But there is more to it, see: `strans -h`

# Extending the `strans`
The `strsns` is written in a very basic python3, with a slight finctional twist. 
If you need an additional functionality you can ... add the funciton.
That funciton needs to have a name - this will automatically be a name of the command.
It needs to process the command line argumnts to that function (they contain the function name as well), and return the transfromation function.

E.g. you want a funciton `comment` that would print the `#` in front of element that contain a substring.
All you need to do is to add a function:
```
def commnt(args):
   """Puts the comment mark # before elements containg a substring"""  # writing the doc string serves as the documentation when -h option is used
   req = args.split()[1] # the required substring needs to follow the comment keyword, maybe you want to have an option to choose what the comment character is? Just add it.
   
   return lambda input: [ '#'+i if req in i elese i for i in input ] # return the transfromation fucntion (quite trivial in this case)
```

And do not forget to share your nice extensions.
