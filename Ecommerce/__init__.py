# import accelerate
# import transformers
# import json
#
# REPO_ID = "/home/robertwang/w-7b-hf"
# # Show that when we do this neither GPU nor CPU memory increases
# config = transformers.AutoConfig.from_pretrained(REPO_ID)
#
# # This device map was generated using accelerator.infer_auto_device_map() function
# device_map = {
#     'model.embed_tokens': 0,
#      'model.layers.0': 0,
#      'model.layers.1': 0,
#      'model.layers.2': 0,
#      'model.layers.3': 0,
#      'model.layers.4': 0,
#      'model.layers.5': 0,
#      'model.layers.6': 0,
#      'model.layers.7': 0,
#      'model.layers.8': 0,
#      'model.layers.9': 0,
#      'model.layers.10': 0,
#      'model.layers.11': 0,
#      'model.layers.12': 0,
#      'model.layers.13': 0,
#      'model.layers.14': 0,
#      'model.layers.15': 0,
#      'model.layers.16': 0,
#      'model.layers.17': 0,
#      'model.layers.18': 0,
#      'model.layers.19': 0,
#      'model.layers.20': 0,
#      'model.layers.21': 0,
#      'model.layers.22': 0,
#      'model.layers.23': 0,
#      'model.layers.24': 0,
#      'model.layers.25': 0,
#      'model.layers.26': 0,
#      'model.layers.27': 0,
#      'model.layers.28': 0,
#      'model.layers.29': 0,
#      'model.layers.30': 0,
#      'model.layers.31': 0,
#      'model.norm': 0,
#      'lm_head': 0
# }
#
# model = transformers.LlamaForCausalLM.from_pretrained(
#         REPO_ID,
#         device_map=device_map,
#         offload_folder="/tmp/.offload",
#         load_in_8bit=True,
#         llm_int8_enable_fp32_cpu_offload=True,
#     )
#
# print("Load successfully.")