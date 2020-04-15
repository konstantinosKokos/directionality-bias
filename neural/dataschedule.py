from torch.utils.data import Dataset, DataLoader
from DirectionalityBias.data.make_dataset import *

from typing import TypeVar, List

DataPoint = Tuple[Expr, int]
DataPoints = List[DataPoint]


class ScheduleSet(Dataset):
    def __init__(self, data: DataPoints):
        self._data = data
        self.epoch = 0
        self.epoch_data = None

    def update_valid(self, update_fn: Callable[[int], Callable[[DataPoint], bool]]) -> None:
        self.epoch += 1
        filter_fn = update_fn(self.epoch)
        self.epoch_data = list(filter(filter_fn, self._data))

    def __len__(self) -> int:
        return len(self.epoch_data) if self.epoch_data is not None else 0

    def __getitem__(self, item: int) -> DataPoint:
        return self.epoch_data[item]


def max_len_per_epoch(epoch: int, epoch_to_len: Callable[[int], int]) -> Callable[[DataPoint], bool]:
    this_epoch_len = epoch_to_len(epoch)

    def filter_fn(datapoint: DataPoint) -> bool:
        return True if len(datapoint[0]) < this_epoch_len else False

    return filter_fn

