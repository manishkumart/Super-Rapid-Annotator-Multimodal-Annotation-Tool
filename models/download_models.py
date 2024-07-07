import argparse
from huggingface_hub import snapshot_download

def download_models(model1_path, model2_path):
    snapshot_download(repo_id="Chat-UniVi/Chat-UniVi", local_dir=model1_path)
    snapshot_download(repo_id="microsoft/Phi-3-mini-128k-instruct", local_dir=model2_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download models to specified paths.')
    parser.add_argument('--m1', type=str, required=True, help='Path to download Model 1 (Chat-UniVi).')
    parser.add_argument('--m2', type=str, required=True, help='Path to download Model 2 (Phi-3-mini-128k-instruct).')

    args = parser.parse_args()
    download_models(args.m1, args.m2)
