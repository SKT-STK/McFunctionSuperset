a pugin for beet/bolt which adds:  
retaining entity and location execution context for /schedule if 'as @s' is present in the same line,  
"fixes" /execute anchored eyes by adding "positioned ^ ^ ^" after it  

it should come last in the pipeline and the two functions can be enabled separatly, it is to be noted however, that "skt_stk.anchored" should come second to ".schedule"  

!!! AT THIS MOMENT VERY VERY EXPERIMENTAL AND PROB HAS A 1_000_000 EDGE-CASES WHERE IT WONT WORK !!!,
