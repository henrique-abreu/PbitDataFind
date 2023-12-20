import subprocess
import os
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile
import json

# Working Directort
wd = os.getcwd()
wd_reports = wd + "/Reports/"
wd_reports_land = wd + "/Reports_land/"
wd_reports_stg = wd + "/Reports_stg/"

# All files from the Reports
onlyfilesReports = [f for f in listdir(wd_reports) if isfile(join(wd_reports, f))]

# Extract schema

failed_reports = []

print("Starting Extracting")

for file in onlyfilesReports:

    filename = file.split('.')[0]

    try:
        with ZipFile(wd_reports + file, 'r') as zObject:  
            zObject.extract("DataModelSchema", path=f"{wd_reports_land}") 
        zObject.close()

        os.rename(wd_reports_land + "DataModelSchema", wd_reports_land + f"{filename}")
    except KeyError:
        failed_reports.append(file)

print("\nEnding Extracting")

# Stage files

print("\nStarting Json Conversion")

onlyfilesReports = [f for f in listdir(wd_reports_land) if isfile(join(wd_reports_land, f))]

for file in onlyfilesReports:

    powershell_script = f'''
        Get-Content "{wd_reports_land + file}" -Raw -Encoding unicode |
        Out-File -FilePath "{wd_reports_stg + file}.json" -Encoding utf8
    '''

    # Powershell
    subprocess.run(["powershell", "-Command", powershell_script])

print("\nEnding Json Conversion")
print("\nStarting Comparing")
# Read Json
results = []

onlyfilesReports = [f for f in listdir(wd_reports_stg) if isfile(join(wd_reports_stg, f))]
# elementToFind = ["Sprint"]

elementToFind = ["A575", "A575_and_KONP_id", "A575_and_KONP_land", "A575_id", "EKBE", "EKBE_id", "EKBE_land", "EKES", "EKES_hist", "EKES_id", 
           "EKES_land", "EKET", "EKET_id", "EKET_land", "EKKN", "EKKN_id", "EKKN_land", "EKKO", "EKKO_id", "EKKO_land", "EKPO", "EKPO_id", 
           "EKPO_land", "HAOV_DATE", "KONP", "KONP_id", "LFA1", "LFA1_id", "LFA1_land", "MAKT", "MAKT_land", "MARA", "MARA_id", "MARA_land", 
           "MVKE", "MVKE_id", "MVKE_land", "OrderFirstCommitDates", "T023T", "T023T_land", "T134T", "T134T_land", "TPTMT", "TPTMT_land", 
           "TSPAT", "TSPAT_land", "VBAK", "VBAK_id", "VBAK_land", "VBAP", "VBAP_id", "VBAP_land", "ZCSAB", "ZCSAB_land", "ZCTO_TECHHIST", 
           "ZCTO_TECHHIST_id", "ZCTO_TECHHIST_Land", "ZCTOWEBALIGHT", "ZCTOWEBALIGHT_land", "ZCVAS", "ZCVAS_land", "ZKTP_PRDB", 
           "ZKTP_PRDB_land", "ZMG_FAMILIET", "ZMG_FAMILIET_land", "ZMG_MODELLT", "ZMG_MODELLT_land", "ZMG_PRAESKATEGT", "ZMG_PRAESKATEGT_land", 
           "ZMG_SUBKATEGT", "ZMG_SUBKATEGT_land", "ZMTKONFTYP_T", "ZMTKONFTYP_T_land", "ZVLIEF", "ZVLIEF_id", "ZVLIEF_INBOUND", "ZVLIEF_INBOUND_id", 
           "ZVLIEF_INBOUND_land", "ZVLIEF_land", "ZVMHIER", "ZVMHIER_id", "ZVMHIER_land", "ZVSCARD", "ZVSCARD_id", "ZVSCARD_land", 
           "PDS_SAPP84CentralPricing", "PDS_SAPP84ProductBOM", "PDS_SAPP84System", "PDS_SAPP84TC", "PDS_SFDCProduct", "PDS_MaterialByQuote", 
           "vwFixSupplyPurchaseOrders", "vwFixSupplyPurchaseOrdersStatusHistory", "vwFixSupplyReschedules", "vwFixSupplyReschedules_ZCTO_TECHHIST", 
           "vwMaterialByQuote", "vwPDS_MaterialByQuote", "vwPDS_SAPP84CentralPricing", "vwPDS_SAPP84ProductBOM", "vwPDS_SAPP84System", "vwPDS_SAPP84TC", 
           "vwPDS_SFDCProduct", "vwSalesforceVolumes"]


for file in onlyfilesReports:
    with open(f"C:\\YG_Reports\\Reports_stg\\{file}", "rb") as f:
        data = json.load(f)
    
    for dataset in data.get("model").get("tables"):
        
        filtered_data = dataset.get("partitions")[0].get("source").get("expression")[1]

        res = [ele for ele in elementToFind if(ele in filtered_data)]
            
        if res:
            results.append([f"Element: {res}", f"Report: {file}"])
            break

print("\nEnding Comparing")

# Save results

# 1: Save results Success
open(f'{wd}/results.txt', 'w').close()

with open(f'{wd}/results.txt', 'w') as fp:
    for item in results:
        # write each item on a new line
        fp.write("%s\n" % item)

print("\nDone Success Reports")

# 2: Save results Success
open(f'{wd}/results_bad.txt', 'w').close()

with open(f'{wd}/results_bad.txt', 'w') as fp:
    for item in failed_reports:
        # write each item on a new line
        fp.write("%s\n" % item)

print("\nDone Failed Reports")
