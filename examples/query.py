from samplenaming.core.snsummary import SNSummary

print("========== Original Entries ============")
thissummary = SNSummary()
SNSummary.display_entries(thissummary.df, display_style="compact")

print("========== After first screening ============")
ids = thissummary.query_by_key_value_in("History", 1002, reset_df=False)
thissummary.query_display(display_style="Query")

print("========== Contineous screening ============")
ids = thissummary.query_by("Characterization", ["XRD", "SEM"], reset_df=False)
thissummary.query_display(display_style="Query")

#elements = ["Er", "Y"]
#style = "INCLUDE" #option: "EXCLUDE", "EXACT"

### save to file #####
filename = "SNquery_results.csv"
thissummary.query_save(filename=filename)


'''
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
'''
