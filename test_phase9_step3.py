from omni_expense import handle_expense, get_expenses
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_expense("expense add 100 lunch"); check(1,"expense_add",r is not None and "Expense added" in str(r),str(r)[:50])
r=handle_expense("expenses"); check(2,"expense_list",r is not None and "EXPENSES" in str(r),"list vandhuchu")
r=handle_expense("expense total"); check(3,"expense_total",r is not None and "Total" in str(r),str(r)[:50])
r=handle_expense("expense"); check(4,"expense_keyword",r is not None,"keyword works")
r=handle_expense("expense list"); check(5,"expense_list_kw",r is not None,"list kw works")
r=handle_expense("hello"); check(6,"expense_unknown",r is None,"unknown-ku None correct")
r=handle_expense("expense add abc lunch"); check(7,"expense_bad_amount",r is not None and "number" in str(r).lower(),str(r)[:50])
ex=get_expenses(); check(8,"expense_get",isinstance(ex,list) and len(ex)>=1,f"{len(ex)} expenses")
print(f"=== PHASE 9 STEP 3 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
