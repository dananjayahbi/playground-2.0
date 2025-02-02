import torch
import os
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import datasets, transforms
from PIL import Image
import faiss
import numpy as np
from tqdm import tqdm  # Import tqdm for progress bar
import random

# --- Dynamic Sparse Activation (DSA) Gate ---
class DSAGate(nn.Module):
    def __init__(self, in_channels, sparsity=0.1):
        super().__init__()
        self.sparsity = sparsity
        self.gate = nn.Sequential(
            nn.Conv2d(in_channels, 16, 3, padding=1),
            nn.AdaptiveAvgPool2d(1),  # Reduce spatial dimensions to (B, C, 1, 1)
            nn.Flatten(),  # Flatten to shape (B, C)
            nn.Linear(16, in_channels)  # Transform to (B, in_channels)
        )

    def forward(self, x):
        scores = self.gate(x).squeeze()  # (B, C)

        # Compute per-batch threshold, instead of a single global one
        thresholds = torch.quantile(scores, 1 - self.sparsity, dim=1, keepdim=True)  # (B, 1)

        mask = (scores > thresholds).float()  # (B, C)

        # Ensure the mask is reshaped properly to match (B, C, H, W)
        return x * mask.view(x.shape[0], x.shape[1], 1, 1)  # Correct broadcasting

# --- Associative Memory Module (AMM) ---
class AMM(nn.Module):
    def __init__(self, prototype_dim):
        super().__init__()
        self.prototype_dim = prototype_dim
        self.prototypes = faiss.IndexFlatL2(prototype_dim)
        self.prototype_data = []

    def add_prototypes(self, embeddings):
        embeddings_np = embeddings.detach().cpu().numpy().astype('float32')

        # Reset FAISS index to avoid duplicate entries
        self.prototypes.reset()

        if len(self.prototype_data) == 0:
            self.prototypes.add(embeddings_np)
        else:
            self.prototypes.add(np.concatenate([self.prototype_data[-1], embeddings_np]))

        self.prototype_data.append(embeddings_np)

    def forward(self, x):
        if len(self.prototype_data) == 0:
            raise RuntimeError("No prototypes available in FAISS. Ensure prototypes are added before training.")

        x_np = x.detach().cpu().numpy().astype('float32')

        # Ensure FAISS index has prototypes
        if self.prototypes.ntotal == 0:
            raise RuntimeError("FAISS index is empty! No prototypes were added.")
        
        MIN_PROTOTYPES = 10  # Adjust this value if needed

        if self.prototypes.ntotal < MIN_PROTOTYPES:
            raise RuntimeError(f"Not enough prototypes for FAISS search. Found {self.prototypes.ntotal}, but need at least {MIN_PROTOTYPES}.")

        # Perform FAISS search
        _, indices = self.prototypes.search(x_np, 1)

        # Ensure indices are within bounds
        valid_indices = [idx[0] for idx in indices if 0 <= idx[0] < len(self.prototype_data[0])]

        if len(valid_indices) == 0:
            raise RuntimeError(f"FAISS returned invalid indices. Expected range: 0-{len(self.prototype_data[0])-1}, Got: {indices}")

        return torch.stack([torch.from_numpy(self.prototype_data[0][idx]) for idx in valid_indices]).to(x.device)

# --- Main Network ---
class NDSPC_CatDetector(nn.Module):
    def __init__(self, img_size=64):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.dsa_gate = DSAGate(16, sparsity=0.2)
        
        # Calculate prototype dimension based on conv1 output
        with torch.no_grad():
            dummy_input = torch.zeros(1, 3, img_size, img_size)
            features = self.conv1(dummy_input)
            self.prototype_dim = features.numel() // features.shape[0]
        
        self.amm = AMM(self.prototype_dim)
        self.predictor = nn.Linear(self.prototype_dim, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.dsa_gate(x)
        x_flat = x.view(x.size(0), -1)
        prototype = self.amm(x_flat)
        return torch.sigmoid(self.predictor(prototype)).squeeze()

# Hyperparameters
SPARSITY = 0.2
LR = 0.001
BATCH_SIZE = 8
IMG_SIZE = 64
torch.backends.cudnn.benchmark = True  # Optimize performance

if torch.cuda.is_available():
    DEVICE = "cuda:0"
    torch.cuda.empty_cache()  # Clears any cached memory
else:
    DEVICE = "cpu"

print(f"Using device: {DEVICE}")

# Data Loading
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])

train_dataset = datasets.ImageFolder("data/train", transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Initialize Model
model = NDSPC_CatDetector(img_size=IMG_SIZE).to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# 🔹 Fix OpenMP conflict
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 🔹 Limit FAISS OpenMP threads to avoid conflicts
faiss.omp_set_num_threads(4)

# 🔹 Reduce PyTorch thread usage (Intel CPUs)
torch.set_num_threads(4)

# Phase 1: Prototype Learning with Progress Bar
print("Pretraining prototypes...")
model.eval()
with torch.no_grad():
    for images, _ in tqdm(train_loader, desc="Building Prototypes", unit="batch"):
        images = images.to(DEVICE)
        features = model.conv1(images)
        features_flat = features.view(features.size(0), -1)
        model.amm.add_prototypes(features_flat)

# Print FAISS Index Size
print(f"Total prototypes added: {len(model.amm.prototype_data)}")
print(f"FAISS index size: {model.amm.prototypes.ntotal}")  # Check FAISS index


# Phase 2: Supervised Training with Progress Bar
print("Fine-tuning...")
model.train()
criterion = nn.BCELoss()

for epoch in range(20):
    total_loss = 0
    progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}", unit="batch")
    
    for images, labels in progress_bar:
        images, labels = images.to(DEVICE), labels.float().to(DEVICE)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Simplified Hebbian-inspired update
        loss.backward()
        
        # Apply sparsity mask to gradients
        with torch.no_grad():
            for name, param in model.named_parameters():
                if "conv1.weight" in name and param.grad is not None:  # ✅ Check if grad exists
                    grad_mask = (param != 0).float()
                    param.grad *= grad_mask  # Only apply mask if grad is not None
        
        optimizer.step()
        total_loss += loss.item()
        
        # Update progress bar with current loss
        progress_bar.set_postfix(loss=f"{loss.item():.4f}")
    
    print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")

# Test function
def predict_cat(image_path):
    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(DEVICE)
    model.eval()
    with torch.no_grad():
        prob = model(img_tensor).item()
    return "Cat" if prob > 0.5 else "Non-Cat"

# Example Prediction
print(predict_cat("./tmp/ct1.jpg"))
