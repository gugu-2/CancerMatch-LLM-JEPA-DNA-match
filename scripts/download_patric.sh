#!/bin/bash
# Script to download PATRIC genomes/AMR data

TARGET_DIR="../../data/patric"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR" || exit 1

echo "Downloading PATRIC AMR data..."
wget -qO PATRIC_genomes_AMR.txt ftp://ftp.patricbrc.org/patric2/current_release/RELEASE_NOTES/PATRIC_genomes_AMR.txt

echo "PATRIC dataset downloaded successfully to $TARGET_DIR."
