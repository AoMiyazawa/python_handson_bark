from database.database import DatabaseManager
from datetime import datetime
from zoneinfo import ZoneInfo
import sys

db = DatabaseManager('bookmarks.db')


class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table('bookmarks', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'memo': 'text',
            'date_added': 'text not null'
        })


class AddBookmarkCommand:
    def execute(self, data: dict):
        db.add('bookmarks', {
            "title": data["title"],
            "url": data["url"],
            "memo": data["memo"],
            "date_added": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()
        })
        return('Adding Bookmark has completed successfully')


class ListBookmarksCommand:
    def __init__(self, order_by: str = "date_added") -> None:
        self.order_by = order_by

    def execute(self):
        """
        ブックマークの一覧を取得
        引数で並び順を指定
        """
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    def execute(self, data):
        db.delete('bookmarks', {"id": data})
        return "Bookmark deleted successfully!"


class QuiteCommand:
    def execute(self):
        sys.exit()
