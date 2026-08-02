import torch
import torch.nn as nn
import copy

class BioEncoder(nn.Module):
    """
    Standard Transformer Encoder for DNA/Protein Sequences.
    Translates k-mers into continuous vector representations.
    """
    def __init__(self, vocab_size=64, embed_dim=256, num_heads=8, num_layers=6):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
    def forward(self, x):
        x = self.embedding(x)
        return self.transformer(x)


class BioPredictor(nn.Module):
    """
    The JEPA Predictor Network.
    Takes the Context representation and predicts the Latent representation of the Target (masked) region.
    """
    def __init__(self, embed_dim=256, num_heads=8, num_layers=4):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
    def forward(self, context_rep, mask_tokens):
        # Concatenate context representation with mask tokens representing the target regions
        x = torch.cat([context_rep, mask_tokens], dim=1)
        predictions = self.transformer(x)
        return predictions


class BioJEPA(nn.Module):
    """
    Joint-Embedding Predictive Architecture (JEPA) for Biological Sequences.
    Designed by Yann LeCun (Meta).
    This architecture learns the 'latent semantics' of DNA evolution by predicting missing blocks 
    in an abstract embedding space, rather than forcing the model to guess exact nucleotide tokens (like an LLM).
    """
    def __init__(self, vocab_size=64, embed_dim=256):
        super().__init__()
        
        # 1. The Context Encoder (Processes the visible parts of the DNA)
        self.context_encoder = BioEncoder(vocab_size, embed_dim)
        
        # 2. The Target Encoder (Processes the hidden/masked parts of the DNA to create the 'ground truth' latent target)
        self.target_encoder = copy.deepcopy(self.context_encoder)
        
        # Disable gradient updates for the target encoder (Updated via Exponential Moving Average instead)
        for param in self.target_encoder.parameters():
            param.requires_grad = False
            
        # 3. The Predictor (Attempts to guess the Target's latent embedding from the Context's latent embedding)
        self.predictor = BioPredictor(embed_dim)
        
        # Loss Function: Smooth L1 or Cosine Similarity in Latent Space
        self.loss_fn = nn.SmoothL1Loss()
        
    def update_target_encoder(self, momentum=0.996):
        """
        Updates the Target Encoder weights via Exponential Moving Average (EMA) of the Context Encoder weights.
        This prevents representation collapse.
        """
        with torch.no_grad():
            for param_q, param_k in zip(self.context_encoder.parameters(), self.target_encoder.parameters()):
                param_k.data = param_k.data * momentum + param_q.data * (1. - momentum)

    def forward(self, context_dna, target_dna, mask_tokens):
        """
        Forward pass for training the BioJEPA model.
        """
        # 1. Get Latent Representation of the Context
        context_rep = self.context_encoder(context_dna)
        
        # 2. Get Ground Truth Latent Representation of the Target (No Gradients)
        with torch.no_grad():
            target_rep = self.target_encoder(target_dna)
            
        # 3. Predict the Target's Latent Representation
        predicted_target_rep = self.predictor(context_rep, mask_tokens)
        
        # 4. Calculate Loss strictly in Latent Space
        loss = self.loss_fn(predicted_target_rep, target_rep)
        
        return loss, predicted_target_rep
