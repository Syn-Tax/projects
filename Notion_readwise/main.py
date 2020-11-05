#!/usr/bin/env python3

from notion.client import NotionClient
from notion.block import TextBlock
import time

update_time = 60

with open("data.txt", "r") as f:
    data = f.read().split("\n")
    token = data[0]
    read_later_id = data[1]
    highlights_id = data[2]
    
client = NotionClient(token_v2=token)

while True:
    read_later = client.get_collection_view(read_later_id)
    highlights = client.get_collection_view(highlights_id)
    
    highlight_titles = [r.title for r in highlights.collection.get_rows()]

    for i, row in enumerate(read_later.collection.get_rows()):
        if row.title not in highlight_titles:
            added = highlights.collection.add_row()
            added.title = row.title

        highlight_blocks = [b.title for b in highlights.collection.get_rows()[i].children]

        new_blocks = []

        for block in row.children:
            if block.type == "text":
                if block.title not in highlight_blocks and block.get(path="format.block_color"):
                    new_blocks.append(block.title)

        page = highlights.collection.get_rows()[i]

        if highlight_blocks == [] and new_blocks == []:
            page.empty = True

        for block in new_blocks:
            new_block = page.children.add_new(TextBlock, title=block)
            page.empty = False
            print("Highlights updated")

    time.sleep(update_time)

