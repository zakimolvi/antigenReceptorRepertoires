"""
Use OLGA to compute generation probabilities of identified TCR alpha and beta chains

Notes from Olga docs (https://github.com/statbiophys/OLGA):
-CDR3 is strictly defined as "C....F/W". This seems consistent with MiXCR.
"""
import olga.load_model as load_model
import olga.generation_probability as pgen
import olga.sequence_generation as seq_gen
import pandas as pd

#Define the files for loading in generative model/data
olga_path = '/opt/anaconda3/lib/python3.8/site-packages/olga/'
beta_params_file_name = olga_path + 'default_models/human_T_beta/model_params.txt'
beta_marginals_file_name = olga_path + 'default_models/human_T_beta/model_marginals.txt'
beta_V_anchor_pos_file = olga_path + 'default_models/human_T_beta/V_gene_CDR3_anchors.csv'
beta_J_anchor_pos_file = olga_path + 'default_models/human_T_beta/J_gene_CDR3_anchors.csv'

alpha_path = olga_path + 'default_models/human_T_alpha/'
alpha_params =  alpha_path + 'model_params.txt'
alpha_marginals = alpha_path + 'model_marginals.txt'
alpha_V_anchor = alpha_path + 'V_gene_CDR3_anchors.csv'
alpha_J_anchor = alpha_path + 'J_gene_CDR3_anchors.csv'

#Load data
beta_genomic_data = load_model.GenomicDataVDJ()
beta_genomic_data.load_igor_genomic_data(beta_params_file_name, beta_V_anchor_pos_file, beta_J_anchor_pos_file)

alpha_genomic_data = load_model.GenomicDataVJ()
alpha_genomic_data.load_igor_genomic_data(alpha_params, alpha_V_anchor, alpha_J_anchor)

#Load model
beta_generative_model = load_model.GenerativeModelVDJ()
beta_generative_model.load_and_process_igor_model(beta_marginals_file_name)

alpha_generative_model = load_model.GenerativeModelVJ()
alpha_generative_model.load_and_process_igor_model(alpha_marginals)

#Process model/data for pgen computation by instantiating GenerationProbabilityVDJ
pgen_beta = pgen.GenerationProbabilityVDJ(beta_generative_model, beta_genomic_data)
pgen_alpha = pgen.GenerationProbabilityVJ(alpha_generative_model, alpha_genomic_data)

#reference TCRs collected from TCR3d database
df = pd.read_excel('reference_TCRs.xlsx')
df['cdr3a_pgens'] = [pgen_alpha.compute_aa_CDR3_pgen(x) if type(x) == str else None for x in df['CDR3a']]
df['cdr3b_pgens'] = [pgen_beta.compute_aa_CDR3_pgen(y) for y in df['CDR3b']]
df.to_csv('reference_TCRs_pgen.csv') 
