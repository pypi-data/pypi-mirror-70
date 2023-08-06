# Lamb 🐑: Concise Function Expression in Python
This module introduces a new way to express small functions in a compact and intutive way using a single object called `lamb`. Any expression in which a `lamb` appears turns into a function of which `lamb` is a parameter. Check `demo.py` to see a demonstration:

```python
from lamb import *
# Primary purpose: Creating small anonymous functions
res = filter(lamb % 5 < 3, range(30))

# Arbitrary arithmetic and boolean operators are allowed:
f   = (lamb ** 2 % 6) - 28 != 5 / 4
f_l = lambda x: (x ** 2 % 6) - 28 != 5 / 4
f(2) == f_l(2) # The two expressions are equivalent

# Empty function calls, index and attribute access are possible as well
g = lamb().x[2] - 3 == None

# Lambs can be chained with other functions using the righshift operator
h = g >> f >> lamb + 2 # make sure the first function is a lamb

# For multi-variable lambs, different lamb names improve clarity
from lamb.vs import * # Imports a, b, c, ..., z
from lamb.l_vs_ import * # Import l_a_, l_b_, .. arbitrary pre- and postfixes are possible
g = (l_a_ - b) * c

# g is now a function of three arguments, or rather: functions returning functions,
# with one argument each (shoutout to Haskell)
g(1)(2)(3) == g(1, 2)(3) == g(1, 2, 3)

# Arguments replace lambs left-to-right. The following will output -3:
g(1, 2, 3)

# Note that `a_ is b_` and `a_ is lamb`; they differ only in their identifier. 
# In other words, the following are equivalent:
g2 = (lamb - lamb) * lamb
g(1, 2, 3) == g2(1, 2, 3)

# Lambs can be nested. Parents inherit un-evaluated lambs from their children.
# For clarity, lambs can be added as placeholder for unevaluated args:
h  = g(1, 2) + g(3) 
h2 = g(1, 2, a) + g(3, a, b)
h(1, 2, 3) == h2(1, 2, 3)

# In a select few cases, this will work, but is discouraged. Use g = lamb >> f instead.
f = lambda x: x + 2 == 5
g = f(lamb)
f(2) == g(2)
```

## Installation
`lamb` is installable from PyPI:

```
python -m pip install lamb
```