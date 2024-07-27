import json

# 读取操作序列文件
def load_sequence(file_path):
    with open(file_path, 'r') as f:
        sequence = json.load(f)
    return sequence

# 检查evaluate序列是否与基准序列匹配
def check_step_match(meta_step, actual_step):
    return (meta_step['type'] == actual_step['type'] and
            meta_step['element']['resource-id'] == actual_step['element']['resource-id'] and
            meta_step['element']['content-desc'] == actual_step['element']['content-desc'] and
            meta_step['element']['text'] == actual_step['element']['text'])

# 生成 evaluator.json 文件
def generate_evaluator(actions, output_path):
    evaluator = {"actions": actions}
    with open(output_path, 'w') as f:
        json.dump(evaluator, f, indent=4)

def main():
    meta_file = '/Users/yhu33/Desktop/sequences_separate/sequences/P0.Sns.SnsUser.SnsUserShoot#test_post_image_use_camera/2024070800575810-3089-172936/meta.json'  # 替换为实际的meta.json文件路径
    actual_file = '/Users/yhu33/Desktop/sequences_separate/sequences/P0.Sns.SnsUser.SnsUserShoot#test_post_image_use_camera/2024070800575810-3089-172936/meta.json'  # 替换为实际的操作序列文件路径
    output_file = '/Users/yhu33/Desktop/sequences_separate/sequences/P0.Sns.SnsUser.SnsUserShoot#test_post_image_use_camera/2024070800575810-3089-172936/evaluator.json'  # 替换为实际的输出文件路径

    meta_data = load_sequence(meta_file)
    actual_data = load_sequence(actual_file)

    evaluator_actions = []
    for meta_step, actual_step in zip(meta_data, actual_data):
        if check_step_match(meta_step, actual_step):
            action_info = {
                "type": "findaction",
                "match_type": "equal",
                "match_rules": {
                    "action_type": meta_step.get('type'),
                    "resource-id": meta_step['element'].get('resource-id', ''),
                    "content-desc": meta_step['element'].get('content-desc', ''),
                    "text": meta_step['element'].get('text', '')
                },
                "check_type": "equal",
                "check_rules": {}
            }
            evaluator_actions.append(action_info)
        else:
            raise ValueError("Actual step does not match the meta step.")
    
    generate_evaluator(evaluator_actions, output_file)
    print(f"Evaluator file generated at {output_file}")

if __name__ == "__main__":
    main()
