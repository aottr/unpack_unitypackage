import logging
import tarsafe
import tempfile
import os
import shutil
import re
from pathlib import Path


def extract(package_path, output_path=None, encoding='utf-8'):
  """
  Extracts a .unitypackage into the current directory
  @param {string} packagePath The path to the .unitypackage
  @param {string} [outputPath=os.getcwd()] Optional output path, otherwise will use cwd
  """
  if not output_path:
    output_path = os.getcwd() # If not explicitly set, WindowsPath("") has no parents, and causes the escape test to fail

  with tempfile.TemporaryDirectory() as tmpDir:
    # Unpack the whole thing in one go (faster than traversing the tar)
    with tarsafe.open(name=package_path, encoding=encoding) as upkg:
      upkg.extractall(tmpDir)

    # Extract each file in tmpDir to final destination
    for dirEntry in os.scandir(tmpDir):
      assetEntryDir = f"{tmpDir}/{dirEntry.name}"
      if not os.path.exists(f"{assetEntryDir}/pathname") or \
          not os.path.exists(f"{assetEntryDir}/asset"):
        continue #Doesn't have the required files to extract it

      # Has the required info to extract
      # Get the path to output to from /pathname
      with open(f"{assetEntryDir}/pathname", encoding=encoding) as f:
        pathname = f.readline()
        pathname = pathname[:-1] if pathname[-1] == '\n' else pathname #Remove newline
        # Replace windows reserved chars with '_' that arent '/'
        if os.name == 'nt':
          pathname = re.sub(r'[\>\:\"\|\?\*]', '_', pathname)

      # Figure out final path, make sure that it's inside the write directory
      assetOutPath = os.path.join(output_path, pathname)
      if Path(output_path).resolve() not in Path(assetOutPath).resolve().parents:
        print(f"WARNING: Skipping '{dirEntry.name}' as '{assetOutPath}' is outside of '{output_path}'.")
        continue

      #Extract to the pathname
      print(f"Extracting '{dirEntry.name}' as '{pathname}'")
      os.makedirs(os.path.dirname(assetOutPath), exist_ok=True) #Make the dirs up to the given folder
      shutil.move(f"{assetEntryDir}/asset", assetOutPath)

