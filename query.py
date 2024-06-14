from samplenaming.core.snsummary import SNSummary

print("========== Original Entries ============")
thissummary = SNSummary()
SNSummary.display_entries(thissummary.df, display_style="compact")

print("========== After first screening ============")
elements = ["H"]
style = "INCLUDE" #option: "EXCLUDE"
ids = thissummary.query_by_elements(elements, style=style, reset_df=False)
thissummary.query_display(display_style="compact")

print("========== Continueous screening ============")
key = "Elements"
thisvalue = ["HO"]
ids = thissummary.query_by(key, thisvalue)
display_cols = ["Composition", "Synthesize", "Syn_params", "QRcode"]
thissummary.query_display(display_style=display_cols)


### save to file #####
filename = "SNquery_results.csv"
thissummary.query_save(filename=filename)


listfunc = dir(thissummary)
funcs = []
for func in listfunc:
    if "query" in func:
        funcs.append(func)
print("---- list of query methods ----")
print(str(funcs))
print("-------------------------------")


from samplenaming.core.snglobal import CSV_HEADERS, CSV_HEADERS_SHORT
print("available keys")
print(CSV_HEADERS)
print("===========")
print("short list of keys for 'compact' display")
print(CSV_HEADERS_SHORT)