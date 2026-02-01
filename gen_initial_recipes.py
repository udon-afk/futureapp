import json
import os
from datetime import datetime

class RecipeExporter:
    def __init__(self, output_dir="../../liasfile/openclaw-hub/recipes"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_recipe(self, title, description, steps, dependencies=None, verification=""):
        recipe_id = f"recipe_{title.lower().replace(' ', '_').replace('-', '_')}"
        recipe = {
            "version": "1.0",
            "recipe_id": recipe_id,
            "title": title,
            "description": description,
            "author": "Ria & Udon",
            "compatibility": {
                "os": ["linux"],
                "wsl": True,
                "min_vram_gb": 4
            },
            "dependencies": dependencies or {"apt": [], "pip": [], "openclaw_plugins": []},
            "steps": steps,
            "verification": verification
        }
        
        filename = f"{recipe_id}.json"
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(recipe, f, ensure_ascii=False, indent=2)
        
        return recipe

exporter = RecipeExporter()

# 1. セキュリティ強化
r1 = exporter.create_recipe(
    title="OpenClaw Security Hardening",
    description="Gatewayのアクセス制限とログの機密情報マスクを実施する基本セット",
    steps=[
        {"order": 1, "type": "command", "content": "chmod 700 ~/.openclaw", "explanation": "設定ファイルを所有者以外から保護"},
        {"order": 2, "type": "config_patch", "content": "{\"logging\": {\"redactSensitive\": \"tools\"}}", "explanation": "ログの機密情報を自動で隠す"}
    ],
    verification="ls -ld ~/.openclaw の結果が drwx------ であること"
)

# 2. TODOダッシュボード
r2 = exporter.create_recipe(
    title="Private TODO Dashboard",
    description="FastAPIを使用したパスワード認証付きの自律秘書管理ダッシュボード",
    dependencies={"apt": ["python3-venv"], "pip": ["fastapi", "uvicorn", "psutil"], "openclaw_plugins": []},
    steps=[
        {"order": 1, "type": "command", "content": "mkdir -p todo_app/static todo_app/data", "explanation": "ディレクトリ構造の作成"},
        {"order": 2, "type": "command", "content": "python3 -m venv venv && ./venv/bin/pip install fastapi uvicorn psutil", "explanation": "環境構築"},
        {"order": 3, "type": "write_file", "content": "main.py / index.html", "explanation": "ソースコードの展開"}
    ],
    verification="http://localhost:<PORT> にアクセスして設定したパスワードでログインできること"
)

# 3. 低VRAM向けVC環境
r3 = exporter.create_recipe(
    title="Low-VRAM Hybrid Voice Engine",
    description="VRAM 8GB以下でも動作する、CPU(耳)とGPU(喉)を分担させた音声会話システム",
    dependencies={"apt": ["ffmpeg", "sox"], "pip": ["qwen-tts", "faster-whisper", "py-cord[voice]"], "openclaw_plugins": []},
    steps=[
        {"order": 1, "type": "command", "content": "sudo apt update && sudo apt install -y ffmpeg sox", "explanation": "音声処理の必須ライブラリを導入"},
        {"order": 2, "type": "command", "content": "pip install qwen-tts faster-whisper py-cord[voice]", "explanation": "AIモデル実行用のライブラリを導入"},
        {"order": 3, "type": "command", "content": "python voice_bridge.py --device-tts cuda --device-stt cpu", "explanation": "ハイブリッド構成（喉:GPU / 耳:CPU）で起動"}
    ],
    verification="!speak コマンドでVCからリアの声が聞こえること"
)

print(json.dumps([r1, r2, r3], ensure_ascii=False, indent=2))
