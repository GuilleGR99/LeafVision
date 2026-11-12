
from __future__ import annotations

import argparse
import csv
import json
import random
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score
from torchvision.models import (
    MobileNet_V3_Small_Weights,
    mobilenet_v3_small,
)

from data.dataset import build_dataloaders


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a MobileNetV3 Small plant classifier."
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Root directory containing the plant image classes.",
    )
    parser.add_argument(
        "--splits-dir",
        type=Path,
        default=Path("model/splits"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("model/artifacts"),
    )
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--patience", type=int, default=7)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--num-threads", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)

    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def build_model(num_classes: int) -> nn.Module:
    weights = MobileNet_V3_Small_Weights.DEFAULT
    model = mobilenet_v3_small(weights=weights)

    # Freeze the feature extractor.
    for parameter in model.features.parameters():
        parameter.requires_grad = False

    # Replace the final classification layer.
    in_features = model.classifier[-1].in_features

    model.classifier[-1] = nn.Linear(
        in_features,
        num_classes,
    )

    return model


def train_one_epoch(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> tuple[float, float, float]:
    model.train()

    # Keep the frozen feature extractor in evaluation mode.
    model.features.eval()

    total_loss = 0.0
    predictions = []
    targets = []

    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad(set_to_none=True)

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)

        batch_predictions = outputs.argmax(dim=1)

        predictions.extend(batch_predictions.cpu().tolist())
        targets.extend(labels.cpu().tolist())

    average_loss = total_loss / len(loader.dataset)
    accuracy = accuracy_score(targets, predictions)
    macro_f1 = f1_score(
        targets,
        predictions,
        average="macro",
        zero_division=0,
    )

    return average_loss, accuracy, macro_f1


@torch.inference_mode()
def evaluate(
    model: nn.Module,
    loader: torch.utils.data.DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> tuple[float, float, float]:
    model.eval()

    total_loss = 0.0
    predictions = []
    targets = []

    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        total_loss += loss.item() * images.size(0)

        batch_predictions = outputs.argmax(dim=1)

        predictions.extend(batch_predictions.cpu().tolist())
        targets.extend(labels.cpu().tolist())

    average_loss = total_loss / len(loader.dataset)
    accuracy = accuracy_score(targets, predictions)
    macro_f1 = f1_score(
        targets,
        predictions,
        average="macro",
        zero_division=0,
    )

    return average_loss, accuracy, macro_f1


def save_checkpoint(
    path: Path,
    model: nn.Module,
    class_to_idx: dict[str, int],
    epoch: int,
    val_loss: float,
    val_accuracy: float,
    val_f1: float,
) -> None:
    checkpoint = {
        "architecture": "mobilenet_v3_small",
        "num_classes": len(class_to_idx),
        "class_to_idx": class_to_idx,
        "epoch": epoch,
        "val_loss": val_loss,
        "val_accuracy": val_accuracy,
        "val_macro_f1": val_f1,
        "model_state_dict": model.state_dict(),
    }

    torch.save(checkpoint, path)


def main() -> None:
    args = parse_args()

    if args.epochs < 1 or args.batch_size < 1:
        raise ValueError("Epochs and batch size must be positive.")

    if args.patience < 1 or args.num_threads < 1:
        raise ValueError("Patience and number of threads must be positive.")

    set_seed(args.seed)
    torch.set_num_threads(args.num_threads)

    data_dir = args.data_dir.expanduser().resolve()
    splits_dir = args.splits_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    output_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print(f"Device: {device}")
    print(f"PyTorch version: {torch.__version__}")

    # Load datasets.
    dataloaders, class_to_idx = build_dataloaders(
        data_dir=data_dir,
        splits_dir=splits_dir,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        seed=args.seed,
    )

    num_classes = len(class_to_idx)

    print(f"Number of classes: {num_classes}")
    print(f"Training images: {len(dataloaders['train'].dataset)}")
    print(f"Validation images: {len(dataloaders['validation'].dataset)}")

    # Build model.
    print("\nLoading MobileNetV3 Small...")

    model = build_model(num_classes)
    model = model.to(device)

    trainable_parameters = sum(
        parameter.numel()
        for parameter in model.parameters()
        if parameter.requires_grad
    )

    print(f"Trainable parameters: {trainable_parameters:,}")

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.AdamW(
        filter(
            lambda parameter: parameter.requires_grad,
            model.parameters(),
        ),
        lr=args.learning_rate,
        weight_decay=args.weight_decay,
    )

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=2,
        min_lr=1e-6,
    )

    best_model_path = output_dir / "best_model.pth"
    history_path = output_dir / "training_history.csv"
    classes_path = output_dir / "classes.json"

    classes_path.write_text(
        json.dumps(
            {
                class_name: index
                for class_name, index in class_to_idx.items()
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    best_val_f1 = -1.0
    epochs_without_improvement = 0

    history_fields = [
        "epoch",
        "train_loss",
        "train_accuracy",
        "train_macro_f1",
        "val_loss",
        "val_accuracy",
        "val_macro_f1",
        "learning_rate",
        "epoch_seconds",
    ]

    print("\nStarting training...\n")

    with history_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as history_file:
        writer = csv.DictWriter(
            history_file,
            fieldnames=history_fields,
        )
        writer.writeheader()

        for epoch in range(1, args.epochs + 1):
            start_time = time.perf_counter()

            train_loss, train_accuracy, train_f1 = train_one_epoch(
                model,
                dataloaders["train"],
                criterion,
                optimizer,
                device,
            )

            val_loss, val_accuracy, val_f1 = evaluate(
                model,
                dataloaders["validation"],
                criterion,
                device,
            )

            scheduler.step(val_f1)

            current_lr = optimizer.param_groups[0]["lr"]
            epoch_seconds = time.perf_counter() - start_time

            row = {
                "epoch": epoch,
                "train_loss": round(train_loss, 5),
                "train_accuracy": round(train_accuracy, 5),
                "train_macro_f1": round(train_f1, 5),
                "val_loss": round(val_loss, 5),
                "val_accuracy": round(val_accuracy, 5),
                "val_macro_f1": round(val_f1, 5),
                "learning_rate": current_lr,
                "epoch_seconds": round(epoch_seconds, 2),
            }

            writer.writerow(row)
            history_file.flush()

            print(
                f"Epoch [{epoch:02d}/{args.epochs:02d}] "
                f"| Train loss: {train_loss:.4f} "
                f"| Train acc: {train_accuracy:.4f} "
                f"| Train F1: {train_f1:.4f} "
                f"| Val loss: {val_loss:.4f} "
                f"| Val acc: {val_accuracy:.4f} "
                f"| Val F1: {val_f1:.4f} "
                f"| LR: {current_lr:.2e} "
                f"| Time: {epoch_seconds:.1f}s"
            )

            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                epochs_without_improvement = 0

                save_checkpoint(
                    best_model_path,
                    model,
                    class_to_idx,
                    epoch,
                    val_loss,
                    val_accuracy,
                    val_f1,
                )

                print("  -> Best model saved.")

            else:
                epochs_without_improvement += 1

            if epochs_without_improvement >= args.patience:
                print(
                    f"\nEarly stopping: no improvement for "
                    f"{args.patience} epochs."
                )
                break

    print("\nTraining completed.")
    print(f"Best validation macro-F1: {best_val_f1:.4f}")
    print(f"Best model: {best_model_path}")
    print(f"Training history: {history_path}")
    print(f"Class mapping: {classes_path}")


if __name__ == "__main__":
    main()
