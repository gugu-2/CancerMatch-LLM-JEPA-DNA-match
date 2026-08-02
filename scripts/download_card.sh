#!/bin/bash
# Script to download the Comprehensive Antibiotic Resistance Database (CARD)

TARGET_DIR="../../data/card"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR" || exit 1

echo "Downloading latest CARD data..."
wget -qO card_data.tar.bz2 https://card.mcmaster.ca/latest/data
echo "Extracting CARD data..."
tar -xjf card_data.tar.bz2
rm card_data.tar.bz2

echo "CARD database downloaded and extracted successfully to $TARGET_DIR."
