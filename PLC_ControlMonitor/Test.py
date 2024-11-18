def string_to_hex_with_spaces(input_str):
    """文字列を16進数に変換し、4文字ごとにスペースを挿入"""
    # 文字列を16進数に変換
    hex_str = ''.join([format(ord(char), '02X') for char in input_str])
    
    # 4文字ごとにスペースを挿入
    spaced_hex_str = ' '.join([hex_str[i:i+4] for i in range(0, len(hex_str), 4)])
    
    return spaced_hex_str

# 例: 文字列 "Hello"
input_str = "Hello"

# 変換した16進数の文字列を表示
converted_hex = string_to_hex_with_spaces(input_str)
print(converted_hex)
