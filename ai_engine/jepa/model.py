import torch
import torch.nn as nn

class ContextEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Linear(128, 64)
    def forward(self, x):
        return self.net(x)

class TargetEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Linear(128, 64)
    def forward(self, x):
        with torch.no_grad():
            return self.net(x)

class Predictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Linear(64, 64)
    def forward(self, x):
        return self.net(x)
