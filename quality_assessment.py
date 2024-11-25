import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import cv2
import numpy as np
from pathlib import Path

class QualityNet(nn.Module):
    def __init__(self):
        super(QualityNet, self).__init__()
        # Use ResNet-18 as backbone
        resnet = models.resnet18(pretrained=True)
        # Remove the last fully connected layer
        self.features = nn.Sequential(*list(resnet.children())[:-1])
        # Add quality assessment head
        self.quality_head = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        features = self.features(x)
        features = features.view(features.size(0), -1)
        quality = self.quality_head(features)
        return quality

class QualityAssessor:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = QualityNet().to(self.device)
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])
        
        # Load pre-trained weights if available
        model_path = Path(__file__).parent / 'models' / 'quality_net.pth'
        if model_path.exists():
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def _extract_frames(self, video_path, num_frames=10):
        """Extract evenly spaced frames from video for quality assessment."""
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)
        
        frames = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
        
        cap.release()
        return frames

    def assess_quality(self, video_path):
        """Assess the quality of a video using the ML model."""
        frames = self._extract_frames(video_path)
        if not frames:
            raise ValueError("No frames could be extracted from the video")

        # Process frames through the model
        quality_scores = []
        with torch.no_grad():
            for frame in frames:
                # Prepare input
                input_tensor = self.transform(frame).unsqueeze(0).to(self.device)
                
                # Get quality prediction
                quality_score = self.model(input_tensor).item()
                quality_scores.append(quality_score)

        # Return average quality score
        return np.mean(quality_scores)

    def train(self, train_loader, num_epochs=10):
        """Train the quality assessment model (for future improvements)."""
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        self.model.train()
        for epoch in range(num_epochs):
            for batch_idx, (frames, targets) in enumerate(train_loader):
                frames, targets = frames.to(self.device), targets.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(frames)
                loss = criterion(outputs, targets)
                
                loss.backward()
                optimizer.step()
                
                if batch_idx % 100 == 0:
                    print(f'Epoch: {epoch}, Batch: {batch_idx}, Loss: {loss.item():.4f}')
