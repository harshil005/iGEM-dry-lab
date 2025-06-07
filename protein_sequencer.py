import gzip
from Bio import SeqIO
from pathlib import Path

#path to compessed .gbff files
gbff_dir = Path("ncbi_genomes_gbff")
output_dir = Path("protein_fastas")
output_dir.mkdir(exist_ok=True)


for gbff_file in gbff_dir.glob("*.gbff.gz"):
    strain_name = gbff_file.stem.replace(".gbff", "")
    output_fasta = output_dir / f"{strain_name}_proteins.faa"

    print(f"Processing: {gbff_file.name}")

    with gzip.open(gbff_file, "rt") as handle, open(output_fasta, "w") as fasta_out:
        for record in SeqIO.parse(handle, "genbank"):
            for feature in record.features:
                if feature.type == "CDS" and "translation" in feature.qualifiers:
                    protein_seq = feature.qualifiers["translation"][0]
                    gene_name = feature.qualifiers.get("gene", ["unknown_gene"])[0]
                    product = feature.qualifiers.get("product", ["unknown_product"])[0]
                    locus_tag = feature.qualifiers.get("locus_tag", ["unknown_locus"])[0]

                    fasta_out.write(f">{strain_name}|{locus_tag}|{gene_name}|{product}\n{protein_seq}\n")
