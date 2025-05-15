a pugin for beet/bolt which adds:  
retaining entity and location execution context for `/schedule` if `as @s` is present in the same line,  
"fixes" `/execute anchored eyes` by adding `positioned ^ ^ ^` after it,  
added a way to inline macros using the following syntax: `function(with entity @s):`, `with entity @s` can be any valid mcfunction macro argument, the contents of the macro are defined in the indent block under it,  
added a way to inline schedules using the following syntax: `function(20t):`, `20t` can be any valid schedule delay, the contents of the scheduled function are defined in the indent block under it,  

you can enable/disable `schedule`, `anchored` and `inline` as you please in the `beet.json` file as pipeline elements, plz do note however that `skt_stk.inline` should come before `mecha` and `skt_stk.schedule` as well as `skt_stk.achored` should come after it in said order  

!!! AT THIS MOMENT VERY VERY EXPERIMENTAL AND PROB HAS A 1_000_000 EDGE-CASES WHERE IT WONT WORK !!!,
