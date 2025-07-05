import torch
import esm
from Bio import SeqIO
from pathlib import Path
from tqdm import tqdm

#change to esm2_t48_15B_UR50D() when more power
#handle sequence cap of 1024

model_name = "esm1b_t33_650M_UR50S"
model, alphabet = esm.pretrained.load_model_and_alphabet(model_name)
batch_converter = alphabet.get_batch_converter()
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

input_dir = Path("protein_fastas")
output_dir = Path("esm_embeddings")
output_dir.mkdir(exist_ok=True)


BATCH_SIZE = 2  #decrease when using stronger model/larger sequences


for fasta_file in input_dir.glob("*.faa"):
    #to verify
    print(f"\nProcessing: {fasta_file.name}")

    #get sequences in tuple
    sequences = [(record.id, str(record.seq)) for record in SeqIO.parse(fasta_file, "fasta")]
    embeddings = {}

    with torch.no_grad():
        for i in tqdm(range(0, len(sequences), BATCH_SIZE)):
            batch = sequences[i:i + BATCH_SIZE]
            batch_labels, batch_strs, batch_tokens = batch_converter(batch)
            batch_tokens = batch_tokens.to(device)

            #
            results = model(batch_tokens, repr_layers=[33], return_contacts=False)
            attn = results["attentions"]

            token_representations = results["representations"][33]

            for j, (label, seq) in enumerate(batch):
                seq_len = len(seq)
                # average tokens (excludes [CLS] and [EOS]?)
                embedding = token_representations[j, 1:seq_len + 1].mean(0)
                embeddings[label] = embedding.cpu()


    output_file = output_dir / f"{fasta_file.stem}_esm1b_embeddings.pt"
    torch.save(embeddings, output_file)
    print(f"embeddings in {output_file}")
