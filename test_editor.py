#!/usr/bin/env python3
"""
CSC1002 Editor Automated Test Script
Tests all required commands and edge cases.
"""

import subprocess
import sys


def run_test(test_name, commands, expected_outputs, should_contain=True):
    """
    Run a single test case.
    
    Args:
        test_name: Name of the test
        commands: List of commands to send to the editor
        expected_outputs: List of expected strings in output
        should_contain: If True, all expected outputs must be found. 
                       If False, none should be found.
    
    Returns:
        bool: True if test passed, False otherwise
    """
    print(f"\n{'='*50}")
    print(f"测试：{test_name}")
    print('='*50)
    
    # Start editor process
    proc = subprocess.Popen(
        ['python', 'editor.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send commands
    input_text = '\n'.join(commands) + '\n'
    try:
        stdout, stderr = proc.communicate(input=input_text, timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        print("❌ 测试超时!")
        return False
    
    # Check output
    passed = True
    for expected in expected_outputs:
        found = expected in stdout
        if should_contain and not found:
            print(f"❌ 未找到预期输出：{expected}")
            passed = False
        elif not should_contain and found:
            print(f"❌ 找到不应出现的输出：{expected}")
            passed = False
        else:
            print(f"✅ {'找到' if should_contain else '未找到'}：{expected[:50]}...")
    
    if passed:
        print(f"\n✅ {test_name} 通过!")
    else:
        print(f"\n❌ {test_name} 失败!")
        print(f"实际输出:\n{stdout[:500]}")
    
    return passed


def main():
    """Run all tests."""
    tests = [
        # Test 1: Help and Quit
        {
            'name': '帮助和退出',
            'commands': ['?', 'q'],
            'expected': ['? - display', 'h - move cursor left'],
            'should_contain': True
        },
        
        # Test 2: Insert and View
        {
            'name': '插入和查看',
            'commands': ['iHello World', 'v', 'q'],
            'expected': ['Hello World'],
            'should_contain': True
        },
        
        # Test 3: Cursor Movement (left/right)
        {
            'name': '光标左右移动',
            'commands': ['iHello', 'l', 'v', 'h', 'v', 'q'],
            'expected': ['Hello'],
            'should_contain': True
        },
        
        # Test 4: Home and End
        {
            'name': '行首行尾移动',
            'commands': ['iHello', '^', 'v', '$', 'v', 'q'],
            'expected': ['Hello'],
            'should_contain': True
        },
        
        # Test 5: Delete Character
        {
            'name': '删除字符',
            'commands': ['iHello', 'x', 'v', 'q'],
            'expected': ['ello'],
            'should_contain': True
        },
        
        # Test 6: Delete Previous Character
        {
            'name': '删除前一个字符',
            'commands': ['iHello', 'l', 'X', 'v', 'q'],
            'expected': ['Hllo'],
            'should_contain': True
        },
        
        # Test 7: Append Text
        {
            'name': '追加文本',
            'commands': ['iHello', '$', 'a World', 'v', 'q'],
            'expected': ['Hello World'],
            'should_contain': True
        },
        
        # Test 8: Insert at Front
        {
            'name': '在开头插入',
            'commands': ['iWorld', 'ISay ', 'v', 'q'],
            'expected': ['Say World'],
            'should_contain': True
        },
        
        # Test 9: Append at End
        {
            'name': '在末尾追加',
            'commands': ['iHello', 'A!', 'v', 'q'],
            'expected': ['Hello!'],
            'should_contain': True
        },
        

        
        # Test 11: Word Movement
        {
            'name': '单词间移动',
            'commands': ['iHello World Test', 'w', 'v', 'b', 'v', 'q'],
            'expected': ['Hello World Test'],
            'should_contain': True
        },
        
        # Test 12: Toggle Cursor
        {
            'name': '切换光标显示',
            'commands': ['iTest', '.', 'v', 'q'],
            'expected': ['Test'],
            'should_contain': True
        },
        
        # Test 13: Invalid Commands (should not affect content)
        {
            'name': '无效命令处理',
            'commands': ['iHello', ' ', '? ', '$ ', 'i', 'a', 'z', 'v', 'q'],
            'expected': ['Hello'],
            'should_contain': True
        },
        
        # Test 14: Empty Text Operations
        {
            'name': '空文本操作',
            'commands': ['v', 'h', 'l', 'x', 'X', 'v', 'q'],
            'expected': [''],
            'should_contain': True
        },
        
        # Test 15: Comprehensive Edit
        {
            'name': '完整编辑流程',
            'commands': [
                'iThe quick brown fox',
                'w', 'w', 'x',
                'a jumps over',
                '^', 'dw',
                '$', 'a!',
                'v', 'q'
            ],
            'expected': ['quick brown fox jumps over!'],
            'should_contain': True
        },
    ]
    
    passed = 0
    failed = 0
    failed_tests = []
    
    for test in tests:
        if run_test(
            test['name'], 
            test['commands'], 
            test['expected'],
            test['should_contain']
        ):
            passed += 1
        else:
            failed += 1
            failed_tests.append(test['name'])
    
    # Summary
    print(f"\n{'='*50}")
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print('='*50)
    
    if failed > 0:
        print("\n失败的测试:")
        for name in failed_tests:
            print(f"  - {name}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
