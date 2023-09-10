# Mocked database object for the sake of this example.
class MockDB:
    def get_article(self):
        # In reality, this would be a SQL query.
        return "This is the content of the article."

mockdb = MockDB()