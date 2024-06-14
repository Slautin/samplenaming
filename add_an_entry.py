from samplenaming.core.snsummary import SNSummary

thissummary = SNSummary()
#SNSummary.display_entries(thissummary.df, display_style="compact")

upload_files = None
thissummary.add_an_entry(upload_files=upload_files)
SNSummary.display_entries(thissummary.df, display_style="Full")

upload_files = ["LICENSE", "MANIFEST.in"]
thissummary.add_an_entry(upload_files=upload_files)
SNSummary.display_entries(thissummary.df, display_style="compact")
