# Strings transformations for NIXers

You probably used those NIX programs that let you transform text in the daily work. 
Probably you have your own set of favourite tools ... the `sed`  to replace strings, the `awk` do some more formatting, `cut` - to pick a field ... ah how useful is that one!
But each of them is a bit different, has own syntax of commands, specialities .... well, the history.
What if there would be one simple program that would let you do the transformation we usually need to do.

An example:
You wan to list PDF files in the directory and generate LATEX includegraphics directive for them.
```
ls  | strans "split | cont pdf |cont _q| prep \includegraphics[width=0.3\textwidth]{ | app } | nl"
```
So it starts with the `ls` that output all the file names to stdout. Then `strans` picks up and:
* `split` - splits that into a list
* `cont pdf` - selects those files that have `pdf` in the name
* `cont _q` - selects those containing `_q` (because why not, I want those - and it nicely shows that you can combine the strans commands)
* `prep \include..` - prepends the text to each file name
* `app }` - well, appends the text
* `nl` - outputs the list of elements, each in new line
*

But there is more to it, see: `strans -h`

# Extending the `strans`
It is written in a very basic python3, with a slight finctional twist. 
If you need an additional functionality you can ... add the funciton.
That funciton needs to have a name - this will automatically be a name of the command.
It needs to process the command line argumnts to that function (they contain the function name as well), and return the transfromation function.

E.g. you want a funciton `comment` that would print the `#` in front of element that contain a substring.
All you need to do is to add a function:
```
def commnt(args):
   """Puths the comment mark # before element containg a substring"""  # writing the doc string served as funcitonality documentation when -h is used.
   req = args.split()[1] # the required substring needs to follow the comment keyword
   return lambda input: [ '#'+i if req in i elese i for i in input ] # and the transfromation fucntion (quite trivial in this case)
```

And do not forget to share your nice extensions.
