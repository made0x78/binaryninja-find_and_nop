#!/usr/bin/env python
# Author: made0x78

from binaryninja import PluginCommand
from binaryninja import interaction
from binaryninja import InstructionTextTokenType

def resolved_function_name(addr, bv):
    func = bv.get_function_at(addr)
    if func:
        return func.name
    return ""

def comment(function, address, msg):
    function.set_comment(address, msg)

def check_pattern(pattern, inst, bv):
    for idx_line, line in enumerate(pattern):
        pattern_part_idx = -1
        for idx_part, part in enumerate(inst[idx_line][0]):
            part_text = ""
            if part.text.strip() == "": # skip empty stuff
                continue

            # resolve address if necessary
            if part.type == InstructionTextTokenType.CodeRelativeAddressToken:
                # try to resolve function name
                part_text = resolved_function_name(int(part.text, 16), bv)
                if part_text == None:
                    # try to resolve data segment name by symbol
                    part_text = bv.get_symbol_at(int(part.text, 16))
                    if part_text == None:
                        # set data variable name as default name
                        part_text = "data_" + part.text[2:]
            else:
                part_text = part.text

            pattern_part_idx += 1
            if len(line) <= pattern_part_idx or line[pattern_part_idx] != part_text.strip():
                return False
    return True

def run_plugin(bv):
    patch_text_field = interaction.MultilineTextField("Instruction(s) to convert to nop's (e.g. int3)")
    res = interaction.get_form_input([patch_text_field], 'Find And Nop')

    if res == False:
        return

    lines = patch_text_field.result.split("\n")

    special_characters = ",[]-+*:"
    pattern = []
    for line in lines:
        temp = line
        for char in special_characters:
            temp = temp.replace(char, " " + char + " ")
        # remove double spaces
        temp = ' '.join(temp.split())
        temp = temp.split()
        pattern.append(temp)

    pattern_len = len(pattern)
    for func in bv.functions:
        func_instr_list = list(func.instructions)
        for idx, inst in enumerate(func_instr_list):
            if (idx + pattern_len) > len(func_instr_list):
                # pattern too long for this function set, check next function
                break
            if check_pattern(pattern, func_instr_list[idx:idx+pattern_len], bv):
                for i in range(pattern_len):
                    # original code as comment
                    comment(func, inst[1], "FaN: " + str(pattern))
                    bv.convert_to_nop(func_instr_list[idx+i][1])

    interaction.show_message_box("Possible Reload Required", "Maybe you have to save and reload the binary because the functions aren't updated. E.g. if you have replaced int3 instructions the code flow will change.")
# register plugin
PluginCommand.register("[FaN] Find an assembly pattern and replace it with nop's", "Find and Nop", run_plugin)
