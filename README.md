# Find and Nop
This plugin provides a simple feature to replace assembly patterns with nop's in the whole binary. This can be useful to defeat simple anti debugging features like breakpoints (int3 instructions) or anti vm mechanism which have the same pattern in the given binary.

## Installation
Just copy ```Find and Nop``` folder to your local binary ninja plugin folder.

## Usage
You can trigger the plugin via the right click context menu of binary ninja.

<img src="images/Original_binary_menu.png" height=400 width=500><br>

If you select the plugin, a prompt with a multi line text field appears where you can enter assembly code.<br>
For example:
```
int 3
```
or
```
mov rsi, rax
pop rsi
pop rdi
call strtol
```

<img src="images/Original_binary_fan.png" height=300 width=400><br>

<img src="images/Original_binary_replaced_msg.png" height=300 width=400><br>

After replacing the breakpoints of this sample we can compare the function list of the old and new binary.<br>

### Original
<img src="images/Original_binary_functions.png" height=500 width=140><br>

### Modified
<img src="images/Reloaded_binary_functions.png" height=500 width=140><br><br>
Here you can see the replaced int3 instruction in the modified binary:

<img src="images/Reloaded_binary_nop.png"><br>
