# qtile-swallower
Currently qtile does not support direct first class window swallowing.
While this can be achieved via other ways (for instance with a separate binary swallower such as [Devour](https://github.com/salman-abedin/devour)) this behavior really 
is part of window management and, as such, belongs to wm-adjacent packages/configuration.

As a matter of fact, you can actually achieve window swallowing in qtile with just some configuration (check [Disc#3815](https://github.com/qtile/qtile/discussions/3815) and [Issue#1771](https://github.com/qtile/qtile/issues/1771) for additional info).
This is hack, while pretty cool, requires knowledge of the way X11 treats net\_wm\_pids and to the end user some behaviors (like checking a range of 5 processes) seems completly arbitrary.

In addition to that, to define if, when and which window should be swallowed you have to hack into that algorithm to find a way to skip swallowing in some situations.

This package aims to provide a clear, configurable and declarative way to define swallowing conditions and enable them.
