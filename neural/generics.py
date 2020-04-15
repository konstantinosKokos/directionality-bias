from torch.nn import Module, Embedding
from torch import Tensor, LongTensor
from torch.optim import Optimizer
from torch.utils.data import DataLoader

from typing import List, Any


class Regressor(Module):
    def __init__(self, core: Module):
        super(Regressor, self).__init__()
        self.core = core

    def forward(self, atoms: LongTensor) -> Tensor:
        return self.core(atoms)

    def train_batch(self, batch_x: LongTensor, batch_y: Tensor, loss_fn: Module, optimizer: Optimizer,
                    metrics: List[Module]) -> List[Any]:
        self.train()

        optimizer.zero_grad()

        batch_p = self.forward(batch_x)
        loss = loss_fn(batch_p, batch_y)
        loss.backward()
        optimizer.step()

        return [loss.item()] + [metric(batch_p, batch_y) for metric in metrics]

    def train_epoch(self, dataloader: DataLoader, loss_fn: Module, optimizer: Optimizer, metrics:
                    List[Module]) -> List[List[Any]]:
        return [self.train_batch(batch_x, batch_y, loss_fn, optimizer, metrics)
                for batch_x, batch_y in dataloader]

    def eval_batch(self, batch_x: LongTensor, batch_y: Tensor, loss_fn: Module, metrics: List[Module]) -> List[Any]:
        self.eval()

        batch_p = self.forward(batch_x)
        loss = loss_fn(batch_p, batch_y).item()
        return [loss] + [metric(batch_p, batch_y) for metric in metrics]

    def eval_epoch(self, dataloader: DataLoader, loss_fn: Module, metrics: List[Module]) -> List[List[Any]]:
        return [self.eval_batch(batch_x, batch_y, loss_fn, metrics) for batch_x, batch_y in dataloader]






