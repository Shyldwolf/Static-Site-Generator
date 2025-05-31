from enum import Enum
import re
from typing import List

class BlockType(Enum): # Enum to represent different types of blocks in markdown
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    BLOCKQUOTE = "blockquote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def block_to_block_type(block: str) -> BlockType: # Function to determine the type of a markdown block
    lines = block.split("\n")

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.strip().startswith(">") for line in lines if line.strip()):
        return BlockType.BLOCKQUOTE

    if all(re.match(r"-\s", line) for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(rf"{i+1}\.\s", line) for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING

    return BlockType.PARAGRAPH
