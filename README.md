a pugin for beet/bolt which adds:  


~~retaining entity and location execution context for `/schedule` if `as @s` is present in the same line,~~  
~~"fixes" `/execute anchored eyes` by adding `positioned ^ ^ ^` after it,~~  
- a way to inline macros using the following syntax: `function(with entity @s):`, `with entity @s` can be any valid mcfunction macro argument, the contents of the macro are defined in the indent block under it, like so:  

```
function(with entity @p):  
  $say nearest player's uuid: $(UUID)
```

- a way to inline schedules using the following syntax: `function(20t):`, `20t` can be any valid schedule delay, the contents of the scheduled function are defined in the indent block under it, like so:

```
function(20t):
  say executed after 1sec
```

- a way to inline `/execute if function` statements using the following syntax: `execute if function():` followed by an indent block as the tested function's contents, to continue the execute statement, after the indent block start a line with `;` followed by the rest of the execute command, like so:  

```
execute if function():
  return 1
;run say execute if passed
```

~~you can enable/disable `schedule`, `anchored` and `inline` as you please in the `beet.json` file as pipeline elements,~~ plz do note however that `skt_stk.inline` should come before `mecha` ~~and `skt_stk.schedule` as well as `skt_stk.achored` should come after it in said order~~  

!!! AT THIS MOMENT VERY VERY EXPERIMENTAL AND PROB HAS A 1_000_000 EDGE-CASES WHERE IT WONT WORK !!!,

