from app.models.item import Item
from typing import List, Optional

class ItemService:
    def __init__(self):
        self.items = []
        self.next_id = 1

    def get_all_items(self) -> List[Item]:
        return self.items

    def get_item_by_id(self, item_id: int) -> Optional[Item]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def create_item(self, item: Item) -> Item:
        item.id = self.next_id
        self.next_id += 1
        self.items.append(item)
        return item

    def update_item(self, item_id: int, updated_item: Item) -> Optional[Item]:
        for i, item in enumerate(self.items):
            if item.id == item_id:
                updated_item.id = item_id
                self.items[i] = updated_item
                return updated_item
        return None

    def delete_item(self, item_id: int) -> bool:
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                return True
        return False

item_service = ItemService()