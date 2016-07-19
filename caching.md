Caching
=======

For usual HTTP request, the timestamp of the file has to be compared.

For the templates, it's a bit more tricky since the cached result depends on:

- all included template fragments
- the arguments (not only the file)
- the data, and its last modification date
 
**Simple way:** do not cache ...heck, that's how php does it.

The more efficient way, especially if the page is complex/big:

- when retrieving a template, build 
