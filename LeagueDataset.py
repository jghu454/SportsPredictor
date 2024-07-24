import pandas as pd
import torch
from torch.utils.data import Dataset

class LeagueDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.data_frame = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        # Assuming your data frame has columns for features and one label
        # Adjust column indices as per your CSV file structure
        features = self.data_frame.iloc[idx, :-1].to_numpy(dtype=float)
        label = self.data_frame.iloc[idx, -1]  # Assuming label is the last column
        
        features = torch.tensor(features, dtype=torch.float32)
        label = torch.tensor(label, dtype=torch.long)  # Modify dtype based on your label type

        sample = {'features': features, 'label': label}

        if self.transform:
            sample = self.transform(sample)

        return sample
