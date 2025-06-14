#!/usr/bin/env python3
"""
Download  genome assemblies for strains via the NCBI API.
"""

from Bio import Entrez
import os
import time
from dotenv import load_dotenv

# API key and email
load_dotenv()
Entrez.api_key = os.getenv('API_KEY')
Entrez.email = os.getenv('EMAIL')

# Output directory
download_dir = "ncbi_genomes_gbff"
os.makedirs(download_dir, exist_ok=True)

# List of assemblies
assemblies = [
    "GCF_000209935.1",  # Agathobacter rectalis DSM 17629
    "GCF_025147655.1",  # Blautia hansenii DSM 20583
    "GCF_025147765.1",  # Blautia obeum DSM 25238 // ATCC 29174
    "GCF_025148445.1",  # Butyrivibrio crossotus DSM 2876
    "GCF_000932055.2",  # Clostridium difficile DSM 27543 // 630
#    "GCF_022845755.1",  # Clostridium hylemonae
#    "GCF_000024105.1",  # Clostridium perfringens
    "GCF_014131695.1",  # Clostridium ramosum DSM 1402
#    "GCF_000156295.1",  # Clostridium scindens
    "GCF_011019475.1",  # Clostridium sporogenes NCTC 532
    "GCF_025149785.1",  # Coprococcus comes ATCC 27758
    "GCF_025150245.1",  # Dorea formicigenerans DSM 3994 // ATCC 27755
    "GCF_016889665.1",  # Enterocloster bolteae DSM 15670
    "GCF_029024925.1",  # Enterococcus faecalis DSM 20478
   "GCF_000807675.2",  # Eubacterium limosum DSM 20543 // ACTC 8486
 #   "GCF_000170095.1",  # Eubacterium siraeum DSM 15702
    "GCF_016906045.1",  # Lacrimispora saccharolytica DSM 2544
#    "GCF_030869985.1",  # Lactobacillus crispatus DSM 20356
    "GCF_001908495.1",  # Lactobacillus delbrueckii subsp. delbrueckii DSM 20074
    "GCF_000159215.1",  # Lactobacillus fermentum DSM 20052 (see notes)
    "GCF_000014425.1",  # Lactobacillus gasseri DSM 20243 // ATC 33233
#    "GCF_000078901.1",  # Lactobacillus kefiri SB‑152
#    "GCF_000089012.1",  # Lactobacillus kefiri SB‑227a
#    "GCF_000098123.1",  # Lactobacillus kefiri SB‑376
#    "GCF_000109234.1",  # Lactobacillus paracasei
#   "GCF_000120345.1",  # Lactobacillus plantarum
    "GCF_000224985.1",  # Lactobacillus ruminis // ACTC 27782
    "GCF_001434065.1",  # Lactobacillus sakei subsp. sakei
    "GCF_001435955.1",  # Lactobacillus salivarius DSM 20555
#    "GCF_000164789.1",  # Lactococcus lactis SB‑150
#    "GCF_000175890.1",  # Lactococcus lactis SB‑17
#    "GCF_000186901.1",  # Lactococcus lactis SB‑261
# Leuconostoc mesenteroides
    "GCF_900637905", # Parvimonas micra DSM 20468
    "GCF_000169255.2", # Pseudoflavonifractor capillosus DSM 23940
    "GCF_000225345.1", #Roseburia homninis DSM 16839
    "GCF_900537995.1", #Roseburia intestinalis DSM 14610
    "GCF_020731525.1", # Roseburia inulinivorans DSM 16841
    "GCF_002834225.1", # Ruminococcus bromii ATCC 27255
#    "" # Ruminoccoccus gnavus DSM 108212
    "GCF_000164675.2", # Streptococcus parasanguinis DSM 6778
    "GCF_900636435.1", #Streptococcus salvarius DSM 20560
]


def download_assembly(accession):
    print(f"Processing {accession}...")
    try:
        search_handle = Entrez.esearch(db="assembly", term=accession, retmode="xml")
        search_results = Entrez.read(search_handle)
        search_handle.close()

        if not search_results["IdList"]:
            print(f" {accession} not found")
            return

        assembly_uid = search_results["IdList"][0]

        summary_handle = Entrez.esummary(db="assembly", id=assembly_uid, retmode="xml")
        summary = Entrez.read(summary_handle)
        summary_handle.close()

        docsum = summary['DocumentSummarySet']['DocumentSummary'][0]
        ftp_path = docsum['FtpPath_RefSeq'] or docsum['FtpPath_GenBank']

        if not ftp_path:
            print(f"No FTP path found for {accession}")
            return

        file_name = ftp_path.split('/')[-1]
        genome_url = f"{ftp_path}/{file_name}_genomic.gbff.gz"
        output_path = os.path.join(download_dir, f"{accession}_genomic.gbff.gz")

        if not os.path.exists(output_path):
            os.system(f"curl -L -o {output_path} {genome_url}")
        else:
            print(f"Already downloaded: {output_path}")

        time.sleep(0.5)

    except Exception as e:
        print(f"Error {accession} {e}")

for acc in assemblies:
    download_assembly(acc)

