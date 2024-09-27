def fn_h(k):
    if (k > 0):
         result = k + fn_h(k - 1)
         print(result)
    else:
     result = 0
    return result
print("recursed numbers:")
fn_h(9)