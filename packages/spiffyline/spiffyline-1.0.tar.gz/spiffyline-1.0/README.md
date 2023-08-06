
## Project Description

spiffyline is a terminal utility package that provides formatting,
coloring to terminal output via abstraction of ANSI SGR codes.

Features:

* Abstraction of ANSI SGR codes for ease of use
* Predefined colors for quick formatting
* <code>Theme</code> class to combine SGR codes to reuse
* Utility methods to make adding formatting and color simple and concise

Ussage:

    from spiffyline.theme import Theme
    from spiffyline.logger import Logger

    # Theme with bold and red text
    my_theme = Theme.BOLD + Theme.fg_color( 230, 0, 0 )

    print(  my_theme + "Hello World!" + Theme.RESET )

    # One can also use the Logger class for more concise code

    l = Logger()
    l.log( "Hello World!", my_theme )

    # Or to record certain logging events
    
    l.log( "Error", my_theme, flags=[ "error", ] )
    print( l.events[ "error" ] ) # => 1

Please download the [API Documentation](https://github.com/snakeyworm/spiffylinetree/master/docs) from GitHub
