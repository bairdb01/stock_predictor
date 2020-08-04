import torch
from torch.utils.data import Dataset, DataLoader, random_split
import pandas as pd

class StockDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with stock data
            transform (callable, optional): Optional transform to be applied
        """
        self.price_frame = pd.read_csv(csv_file)
        self.transform = transform

        # Data comes with meaningless OpenInt column
        self.price_frame = self.price_frame.drop(['OpenInt'], axis=1)

    def __len__(self):
        return len(self.price_frame)

    def __getitem__(self, index):
        """
        Data is in the following form:
            Date,Open,High,Low,Close,Volume
        """
        if torch.is_tensor(index):
            index = index.tolist()

        item = self.price_frame.iloc[index]

        sample = {  'date' : item[0],
                    'open_price' : item[1],
                    'day_high' : item[2],
                    'day_low' : item[3],
                    'close_price' : item[4],
                    'volume' : item[5]
                }

        if self.transform:
            sample = self.transform(sample)

        return sample

if __name__ == '__main__':
    # Test loading the dataset and splitting it into test/validation sets
    batch_size = 4
    num_workers = 4

    stock_dataset = StockDataset("sample_data/Stocks/nvda.us.txt")
    train_size = int(len(stock_dataset) * 0.8)
    test_size = int(len(stock_dataset) - train_size)
    training_set, validation_set = random_split( stock_dataset, (train_size, test_size))

    validation_dataloader = DataLoader(validation_set, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    for batch_index, batch in enumerate(dataloader):
        print(batch_index, batch)

    training_dataloader = DataLoader(training_set, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    for batch_index, batch in enumerate(dataloader):
        print(batch_index, batch)
