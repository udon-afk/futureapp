import json
import os

def install_recipe(recipe_path):
    with open(recipe_path, 'r') as f:
        recipe = json.load(f)
    
    print(f"--- Recipe: {recipe['title']} ---")
    print(f"Description: {recipe['description']}")
    print(f"Privileges Required: {recipe['compatibility'].get('required_privileges', 'user')}")
    
    # 1. セキュリティレベルの確認
    print("\n[Security Check]")
    if recipe['dependencies'].get('apt'):
        print(f"The following system packages need to be installed: {recipe['dependencies']['apt']}")
        print("Please run: sudo apt install " + " ".join(recipe['dependencies']['apt']))
    
    # 2. 自動実行可能なステップの提示
    print("\n[Execution Plan]")
    for step in recipe['steps']:
        print(f"{step['order']}. {step['explanation']}")
        # パスワード等の機密情報が含まれる可能性のある表示を抑制
        action_display = step['content']
        if "PASSWORD" in action_display.upper() or "TOKEN" in action_display.upper():
            action_display = "[SENSITIVE CONTENT MASKED]"
        print(f"   Action: {step['type']} -> {action_display}")
    
    print("\nDo you want me to execute the automated steps? (yes/no)")
