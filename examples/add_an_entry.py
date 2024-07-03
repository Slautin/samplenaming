from samplenaming.core.snsummary import SNSummary

thissummary = SNSummary()
SNSummary.display_entries(thissummary.df, display_style="compact")

## add an entry with uploading files
upload_files = ["upload1.txt", "upload2.in"]
thissummary.add_an_entry(upload_files=upload_files)
SNSummary.display_entries(thissummary.df, display_style="Full")

## add an entry based on the previous entry in database
upload_files = None
thissid = 1002
thissummary.add_an_entry_from_id(thissid, upload_files=upload_files)
SNSummary.display_entries(thissummary.df, display_style="Full")

upload_files = ["upload1.txt", "upload2.in"]
thisid = 1003
thissummary.add_an_entry_from_id(thisid, upload_files=upload_files)
SNSummary.display_entries(thissummary.df, display_style="Full")
