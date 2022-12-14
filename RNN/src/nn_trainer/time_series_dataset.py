import numpy
import torch.utils.data


class TimeseriesDataset(torch.utils.data.Dataset):
    """
    Custom Dataset subclass.
    Serves as input to DataLoader to transform X into sequence data using rolling window.
    DataLoader using this dataset will output batches of `(batch_size, seq_len, n_features)` shape.
    Suitable as an input to RNNs.
    """

    def __init__(self, X: numpy.ndarray, y: numpy.ndarray, seq_len: int = 5):
        self.X = torch.tensor(X).float()
        self.y = torch.tensor(y).float()
        self.seq_len = seq_len

    def __len__(self):
        return self.X.__len__() - self.seq_len

    def __getitem__(self, index):
        return self.X[index:index + self.seq_len], self.y[index + self.seq_len]
