from ..database.database import DatabaseManager
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
    def execute(title: str, url: str, memo: str = None):
        db.add('bookmarks', {
            "title": title,
            "url": url,
            "memo": memo,
            "date_added": datetime.now(ZoneInfo("Asia/Tokyo")).isoformat()

        })
        return('Adding Bookmark has completed successfully')


class LIstBookmarksCommand:
    def execute(self, order_by: str = "data_added"):
        return db.select('bookmarks', order_by=order_by).fetchall()


class DeleteBookmarkCommand:
    def execute(self, id: str):
        db.delete('bookmarks', {"id": id})
        return "Bookmark deleted successfully!"


class QuiteCommand:
    def execute(self):
        sys.exit()
